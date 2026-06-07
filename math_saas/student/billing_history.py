import streamlit as st
from typing import Any, Dict, List

from math_saas.utils.db import get_supabase
from math_saas.subscriptions.utils import format_inr, plan_name


def _fetch_user_subscriptions(user_id: str) -> List[Dict[str, Any]]:
    sb = get_supabase()
    res = (
        sb.table("subscriptions")
        .select("*")
        .eq("user_id", user_id)
        .order("started_at", desc=True)
        .execute()
    )
    raw = res.data or []
    return [item for item in raw if isinstance(item, dict)]


def render_billing_history():
    st.header("Billing History")

    student = st.session_state.get("student")
    if not student:
        st.error("Please login as student.")
        return

    user_id = student["id"]
    subs = _fetch_user_subscriptions(user_id)

    if not subs:
        st.info("No billing history yet.")
        return

    rows = []
    for s in subs:
        amount = s.get("amount", 0)
        rows.append(
            {
                "Plan": plan_name(s.get("plan_code", "")),
                "Status": s.get("status", ""),
                "Amount": format_inr(amount),
                "Started": s.get("started_at", ""),
                "Expires": s.get("expires_at", ""),
                "Order ID": s.get("razorpay_order_id", ""),
                "Payment ID": s.get("razorpay_payment_id", ""),
            }
        )

    st.dataframe(rows, width="stretch", hide_index=True)
