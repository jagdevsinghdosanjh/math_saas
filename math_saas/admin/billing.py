import streamlit as st
from typing import Any, Dict, List

from math_saas.auth import require_admin
from math_saas.utils.db import get_supabase
from math_saas.subscriptions.utils import format_inr, plan_name


# ---------------------------------------------------------
# FETCH ALL PAYMENTS (JOINED WITH SUBSCRIPTIONS)
# ---------------------------------------------------------
def _fetch_all_payments() -> List[Dict[str, Any]]:
    sb = get_supabase()

    # Fetch payments with subscription + user info
    res = (
        sb.table("subscription_payments")
        .select(
            """
            id,
            user_id,
            order_id,
            payment_id,
            signature,
            amount,
            status,
            created_at,
            subscriptions:subscription_id (
                plan_code,
                status,
                started_at,
                expires_at,
                razorpay_order_id
            ),
            profiles:user_id (
                full_name,
                email
            )
            """
        )
        .order("created_at", desc=True)
        .execute()
    )

    raw = res.data or []
    return [row for row in raw if isinstance(row, dict)]


# ---------------------------------------------------------
# MAIN BILLING PAGE
# ---------------------------------------------------------
def render():
    require_admin()

    st.title("Billing & Payments")

    payments = _fetch_all_payments()

    if not payments:
        st.info("No payment records found.")
        return

    # Build clean table rows
    rows = []
    for p in payments:
        sub = p.get("subscriptions", {}) or {}
        user = p.get("profiles", {}) or {}

        rows.append(
            {
                "User": user.get("full_name", "") or user.get("email", ""),
                "Plan": plan_name(sub.get("plan_code", "")),
                "Subscription Status": sub.get("status", ""),
                "Payment Status": p.get("status", ""),
                "Amount": format_inr(p.get("amount", 0)),
                "Order ID": p.get("order_id", ""),
                "Payment ID": p.get("payment_id", ""),
                "Started": sub.get("started_at", ""),
                "Expires": sub.get("expires_at", ""),
                "Paid At": p.get("created_at", ""),
            }
        )

    st.subheader("Payments Table")
    st.dataframe(rows, width="stretch", hide_index=True)

    # Inspect raw record
    st.subheader("Inspect Raw Payment Record")

    ids = [str(p.get("id", "")) for p in payments]
    selected_id = st.selectbox("Select Payment ID", ids)

    selected = next((p for p in payments if str(p.get("id", "")) == selected_id), None)
    if selected:
        st.json(selected)
