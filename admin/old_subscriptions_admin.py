import streamlit as st
from typing import Any, Dict, List
from datetime import datetime, timedelta

from auth import require_admin
from utils.db import get_supabase


# ---------------------------------------------------------
# FETCH SUBSCRIPTIONS
# ---------------------------------------------------------
def _fetch_subscriptions(status_filter: str) -> List[Dict[str, Any]]:
    sb = get_supabase()

    query = (
        sb.table("subscriptions")
        .select(
            "id, user_id, plan, plan_code, status, amount, currency, "
            "razorpay_order_id, started_at, expires_at"
        )
        .order("started_at", desc=True)
    )

    if status_filter != "all":
        query = query.eq("status", status_filter)

    res = query.execute()
    raw = res.data or []
    return [row for row in raw if isinstance(row, dict)]


# ---------------------------------------------------------
# ADMIN ACTIONS
# ---------------------------------------------------------
def admin_activate(sub_id: str):
    sb = get_supabase()
    now = datetime.utcnow().isoformat()

    sb.table("subscriptions").update({
        "status": "active",
        "started_at": now,
        "expires_at": (datetime.utcnow() + timedelta(days=30)).isoformat()
    }).eq("id", sub_id).execute()

    return True


def admin_expire(sub_id: str):
    sb = get_supabase()
    sb.table("subscriptions").update({
        "status": "expired",
        "expires_at": datetime.utcnow().isoformat()
    }).eq("id", sub_id).execute()
    return True

def admin_extend(sub_id: str, days: int):
    sb = get_supabase()

    # Fetch current expiry safely
    res = sb.table("subscriptions").select("expires_at").eq("id", sub_id).single().execute()
    data = res.data if isinstance(res.data, dict) else {}

    expires_at_raw = data.get("expires_at")

    # Parse expiry safely
    if isinstance(expires_at_raw, str):
        try:
            current_exp = datetime.fromisoformat(expires_at_raw)
        except ValueError:
            current_exp = datetime.utcnow()
    else:
        current_exp = datetime.utcnow()

    # Add days
    new_exp = current_exp + timedelta(days=days)

    # Update row
    sb.table("subscriptions").update({
        "expires_at": new_exp.isoformat()
    }).eq("id", sub_id).execute()

    return True

# def admin_extend(sub_id: str, days: int):
#     sb = get_supabase()

#     # Fetch current expiry
#     res = sb.table("subscriptions").select("expires_at").eq("id", sub_id).single().execute()
#     current_exp = res.data.get("expires_at")

#     if current_exp:
#         new_exp = datetime.fromisoformat(current_exp) + timedelta(days=days)
#     else:
#         new_exp = datetime.utcnow() + timedelta(days=days)

#     sb.table("subscriptions").update({
#         "expires_at": new_exp.isoformat()
#     }).eq("id", sub_id).execute()

#     return True


def admin_change_plan(sub_id: str, new_plan: str, new_plan_code: str):
    sb = get_supabase()
    sb.table("subscriptions").update({
        "plan": new_plan,
        "plan_code": new_plan_code
    }).eq("id", sub_id).execute()
    return True


# ---------------------------------------------------------
# MAIN ADMIN PAGE
# ---------------------------------------------------------
def render():
    require_admin()

    st.title("Subscription Management")

    # Filter dropdown
    status_filter = st.selectbox(
        "Filter by Status",
        ["all", "active", "pending", "expired", "failed"],
        index=0,
        key="admin_subs_filter"
    )

    subs = _fetch_subscriptions(status_filter)

    if not subs:
        st.info("No subscriptions found for this filter.")
        return

    # Display table
    st.subheader("All Subscriptions")
    st.dataframe(subs, use_container_width=True, hide_index=True)

    # Inspect section
    st.subheader("Inspect Subscription")

    ids = [str(s["id"]) for s in subs]
    selected_id = st.selectbox(
        "Select Subscription ID",
        ids,
        key="admin_subs_select_id"
    )

    selected = next((s for s in subs if str(s["id"]) == selected_id), None)

    if selected:
        st.json(selected)

        st.markdown("---")
        st.subheader("Admin Actions")

        col1, col2, col3, col4 = st.columns(4)

        # Activate
        if col1.button("Activate"):
            admin_activate(selected_id)
            st.success("Subscription activated successfully")

        # Expire
        if col2.button("Expire"):
            admin_expire(selected_id)
            st.warning("Subscription expired")

        # Extend
        extend_days = col3.number_input("Extend (days)", min_value=1, max_value=365, value=30)
        if col3.button("Apply Extension"):
            admin_extend(selected_id, extend_days)
            st.success(f"Extended by {extend_days} days")

        # Change plan
        new_plan = col4.selectbox("New Plan", ["Monthly", "Yearly"])
        new_plan_code = "MTH99" if new_plan == "Monthly" else "YR999"
        if col4.button("Change Plan"):
            admin_change_plan(selected_id, new_plan, new_plan_code)
            st.success(f"Plan changed to {new_plan}")
