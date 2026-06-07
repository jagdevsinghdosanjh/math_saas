import streamlit as st
from typing import Any, Dict, List

from auth import require_admin
from utils.db import get_supabase
from subscriptions.utils import format_inr, plan_name


def _fetch_all_payments() -> List[Dict[str, Any]]:
    sb = get_supabase()
    res = (
        sb.table("subscriptions")
        .select("*")
        .order("started_at", desc=True)
        .execute()
    )
    raw = res.data or []
    return [item for item in raw if isinstance(item, dict)]


def render():
    require_admin()

    st.title("Billing & Payments")

    subs = _fetch_all_payments()

    if not subs:
        st.info("No billing data yet.")
        return

    rows = []
    for s in subs:
        amount = s.get("amount", 0)
        rows.append(
            {
                "User ID": s.get("user_id", ""),
                "Plan": plan_name(s.get("plan_code", "")),
                "Status": s.get("status", ""),
                "Amount": format_inr(amount),
                "Started": s.get("started_at", ""),
                "Expires": s.get("expires_at", ""),
                "Order ID": s.get("razorpay_order_id", ""),
                "Payment ID": s.get("razorpay_payment_id", ""),
            }
        )

    st.subheader("Payments Table")
    st.dataframe(rows, use_container_width=True, hide_index=True)

    st.subheader("Inspect Raw Record")
    ids = [str(s.get("id", "")) for s in subs]
    selected_id = st.selectbox("Select Subscription ID", ids)

    selected = next((s for s in subs if str(s.get("id", "")) == selected_id), None)
    if selected:
        st.json(selected)
