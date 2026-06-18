import streamlit as st
from typing import Any, Dict, List

from auth import require_admin
from utils.db import get_supabase


# ---------------------------------------------------------
# FETCH SUBSCRIPTIONS (TYPE-SAFE)
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

    # Ensure only dict rows are returned
    return [row for row in raw if isinstance(row, dict)]


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
    st.dataframe(subs, width="stretch", hide_index=True)

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
