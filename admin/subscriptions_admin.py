#math_saas/admin/subscriptions_admin.py
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
# SAFE HELPERS
# ---------------------------------------------------------
def _safe_get_dict(data: Any) -> Dict[str, Any]:
    return data if isinstance(data, dict) else {}


def _safe_parse_iso(dt: Any) -> datetime:
    if isinstance(dt, str):
        try:
            return datetime.fromisoformat(dt)
        except Exception:
            return datetime.utcnow()
    return datetime.utcnow()


def _safe_user_id(value: Any) -> str:
    if isinstance(value, str) and value.strip():
        return value
    return ""


# ---------------------------------------------------------
# ADMIN ACTIONS
# ---------------------------------------------------------
def admin_activate(sub_id: str, user_id: str):
    sb = get_supabase()
    now = datetime.utcnow()
    expires = now + timedelta(days=30)

    sb.table("subscriptions").update({
        "status": "active",
        "started_at": now.isoformat(),
        "expires_at": expires.isoformat()
    }).eq("id", sub_id).execute()

    sb.table("profiles").update({
        "subscription_status": "active"
    }).eq("id", user_id).execute()

    return True


def admin_expire(sub_id: str, user_id: str):
    sb = get_supabase()
    now = datetime.utcnow().isoformat()

    sb.table("subscriptions").update({
        "status": "expired",
        "expires_at": now
    }).eq("id", sub_id).execute()

    sb.table("profiles").update({
        "subscription_status": "expired"
    }).eq("id", user_id).execute()

    return True


def admin_extend(sub_id: str, days: int):
    sb = get_supabase()

    res = sb.table("subscriptions").select("expires_at").eq("id", sub_id).single().execute()
    data = _safe_get_dict(res.data)

    current_exp = _safe_parse_iso(data.get("expires_at"))
    new_exp = current_exp + timedelta(days=days)

    sb.table("subscriptions").update({
        "expires_at": new_exp.isoformat()
    }).eq("id", sub_id).execute()

    return True


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

    status_filter = st.selectbox(
        "Filter by Status",
        ["all", "active", "pending", "expired", "failed"],
        index=0,
    )

    subs = _fetch_subscriptions(status_filter)

    if not subs:
        st.info("No subscriptions found for this filter.")
        return

    st.subheader("All Subscriptions")
    st.dataframe(subs, use_container_width=True, hide_index=True)

    st.subheader("Inspect Subscription")

    ids = [str(s["id"]) for s in subs]
    selected_id = st.selectbox("Select Subscription ID", ids)

    selected = next((s for s in subs if str(s.get("id")) == selected_id), None)

    if not selected:
        st.warning("Subscription not found.")
        return

    st.json(selected)

    # Safe user_id extraction
    user_id_raw = selected.get("user_id")
    user_id = _safe_user_id(user_id_raw)

    st.markdown("---")
    st.subheader("Admin Actions")

    col1, col2, col3, col4 = st.columns(4)

    # ACTIVATE
    if col1.button("Activate"):
        if not user_id:
            st.error("Invalid user_id for this subscription.")
        else:
            admin_activate(selected_id, user_id)
            st.success("Subscription activated successfully")

    # EXPIRE
    if col2.button("Expire"):
        if not user_id:
            st.error("Invalid user_id for this subscription.")
        else:
            admin_expire(selected_id, user_id)
            st.warning("Subscription expired")

    # EXTEND
    extend_days = col3.number_input("Extend (days)", min_value=1, max_value=365, value=30)
    if col3.button("Apply Extension"):
        admin_extend(selected_id, extend_days)
        st.success(f"Extended by {extend_days} days")

    # CHANGE PLAN
    new_plan = col4.selectbox("New Plan", ["Monthly", "Yearly"])
    new_plan_code = "MTH99" if new_plan == "Monthly" else "YR999"
    if col4.button("Change Plan"):
        admin_change_plan(selected_id, new_plan, new_plan_code)
        st.success(f"Plan changed to {new_plan}")
