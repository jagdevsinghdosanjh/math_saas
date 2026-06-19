import streamlit as st
from typing import Any, Dict, List, Optional

from auth import require_admin
from utils.db import get_supabase
from subscriptions.utils import format_inr, plan_name


# ---------------------------------------------------------
# FETCH ALL PAYMENTS (JOINED WITH SUBSCRIPTIONS + USERS)
# ---------------------------------------------------------
def _fetch_all_payments() -> List[Dict[str, Any]]:
    sb = get_supabase()

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

    raw = res.data if isinstance(res.data, list) else []
    return [row for row in raw if isinstance(row, dict)]


# ---------------------------------------------------------
# MAIN BILLING PAGE
# ---------------------------------------------------------
def render() -> None:
    require_admin()

    st.title("Billing & Payments")

    payments = _fetch_all_payments()

    if not payments:
        st.info("No payment records found.")
        return

    rows: List[Dict[str, Any]] = []

    for p in payments:
        sub: Dict[str, Any] = p.get("subscriptions") or {}
        user: Dict[str, Any] = p.get("profiles") or {}

        user_display = user.get("full_name") or user.get("email") or "Unknown User"

        rows.append(
            {
                "User": user_display,
                "Plan": plan_name(sub.get("plan_code", "")),
                "Subscription Status": sub.get("status", ""),
                "Payment Status": p.get("status", ""),
                "Amount": format_inr(p.get("amount", 0)),
                "Order ID": p.get("order_id") or "",
                "Payment ID": p.get("payment_id") or "",
                "Started": sub.get("started_at") or "",
                "Expires": sub.get("expires_at") or "",
                "Paid At": p.get("created_at") or "",
            }
        )

    # ---------------------------------------------------------
    # Payments Table
    # ---------------------------------------------------------
    st.subheader("Payments Table")
    st.dataframe(rows, width="stretch", hide_index=True)

    # ---------------------------------------------------------
    # Inspect Raw Payment Record
    # ---------------------------------------------------------
    st.subheader("Inspect Raw Payment Record")

    ids = [str(p.get("id", "")) for p in payments]
    selected_id = st.selectbox("Select Payment ID", ids)

    selected: Optional[Dict[str, Any]] = next(
        (p for p in payments if str(p.get("id", "")) == selected_id),
        None
    )

    if selected:
        st.json(selected)
