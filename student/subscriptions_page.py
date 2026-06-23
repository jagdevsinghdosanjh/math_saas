import streamlit as st
import hmac
import hashlib
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from utils.db import get_supabase, require_user
from subscriptions.utils import plan_name, format_inr
from utils.razorpay import get_razorpay_keys


# ---------------------------------------------------------
# SAFE HELPERS
# ---------------------------------------------------------
def _safe_dict(value: Any) -> Optional[Dict[str, Any]]:
    return value if isinstance(value, dict) else None


# ---------------------------------------------------------
# PAYMENT SUCCESS HANDLER
# ---------------------------------------------------------
def handle_payment_success() -> None:
    params = st.query_params

    payment_id = params.get("payment_id", [""])[0]
    order_id = params.get("order_id", [""])[0]
    signature = params.get("signature", [""])[0]

    if not payment_id or not order_id or not signature:
        st.info("No payment information found.")
        return

    # Validate Razorpay signature
    _, key_secret = get_razorpay_keys()

    generated_signature = hmac.new(
        key_secret.encode(),
        f"{order_id}|{payment_id}".encode(),
        hashlib.sha256,
    ).hexdigest()

    if generated_signature != signature:
        st.error("Payment verification failed. Signature mismatch.")
        return

    sb = get_supabase()

    # Fetch subscription record for this order
    res = (
        sb.table("subscriptions")
        .select("*")
        .eq("razorpay_order_id", order_id)
        .maybe_single()
        .execute()
    )

    sub = _safe_dict(res.data if res else None)
    if not sub:
        st.error("Subscription not found for this payment.")
        return

    sub_id = sub.get("id")
    plan_code = sub.get("plan_code", "")

    # Determine duration
    duration_days = 30 if plan_code == "MTH99" else 365
    now = datetime.utcnow()
    expires = now + timedelta(days=duration_days)

    # Activate subscription
    sb.table("subscriptions").update(
        {
            "status": "active",
            "razorpay_payment_id": payment_id,
            "started_at": now.isoformat(),
            "expires_at": expires.isoformat(),
        }
    ).eq("id", sub_id).execute()

    st.success("Payment successful! Your subscription is now active.")
    st.markdown(
        f"""
        **Payment ID:** {payment_id}  
        **Order ID:** {order_id}  
        **Plan:** {plan_code}  
        **Expires:** {expires.date()}  
        """
    )

    st.page_link("app.py", label="Go to Dashboard")


# ---------------------------------------------------------
# MAIN SUBSCRIPTIONS PAGE
# ---------------------------------------------------------
def render_subscriptions_page() -> None:
    st.header("Subscription")

    # Handle Razorpay callback
    params = st.query_params
    if "payment_id" in params:
        handle_payment_success()
        return

    # Auth
    user_dict = require_user()
    user_id = str(user_dict.get("id", ""))

    sb = get_supabase()

    # Fetch user's subscription
    res = (
        sb.table("subscriptions")
        .select("*")
        .eq("user_id", user_id)
        .maybe_single()
        .execute()
    )

    sub = _safe_dict(res.data if res else None)

    # No subscription record
    if not sub:
        st.warning("You do not have any subscription yet.")
        _render_plan_selection(sb, user_id)
        return

    # Subscription exists but not active
    if sub.get("status") != "active":
        st.warning("You do not have an active subscription.")
        _render_plan_selection(sb, user_id)
        return

    # Active subscription
    plan = plan_name(sub.get("plan_code", ""))
    amount = format_inr(sub.get("amount", 0))
    started = sub.get("started_at", "")
    expires = sub.get("expires_at", "")

    st.success("You have an active subscription.")
    st.markdown(
        f"""
        **Plan:** {plan}  
        **Amount:** {amount}  
        **Started:** {started}  
        **Expires:** {expires}  
        """
    )


# ---------------------------------------------------------
# PLAN SELECTION UI
# ---------------------------------------------------------
def _render_plan_selection(sb: Any, user_id: str) -> None:
    st.subheader("Choose a Plan")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Buy Monthly"):
            _start_checkout(sb, user_id, "MTH99", 9900)

    with col2:
        if st.button("Buy Yearly"):
            _start_checkout(sb, user_id, "YR999", 99900)


# ---------------------------------------------------------
# START CHECKOUT (UPSERT + NAVIGATE)
# ---------------------------------------------------------
def _start_checkout(sb: Any, user_id: str, plan_code: str, amount_paise: int) -> None:
    try:
        res = (
            sb.table("subscriptions")
            .upsert(
                {
                    "user_id": user_id,
                    "plan": "Monthly" if plan_code == "MTH99" else "Yearly",
                    "plan_code": plan_code,
                    "status": "pending",
                    "amount": amount_paise,
                    "currency": "INR",
                    "started_at": None,
                    "expires_at": None,
                    "razorpay_order_id": None,
                },
                on_conflict="user_id",
            )
            .execute()
        )
    except Exception as exc:
        st.error(f"Failed to start checkout. ({exc})")
        return

    data = res.data if res else None
    sub_list = data if isinstance(data, list) else []
    sub = sub_list[0] if sub_list else None

    if not isinstance(sub, dict):
        st.error("Failed to create subscription record.")
        return

    sub_id = sub.get("id")

    # Store subscription ID for checkout page
    st.session_state["sub_id"] = str(sub_id)

    # Navigate to Razorpay checkout page
    st.switch_page("pages/razorpay_checkout.py")
