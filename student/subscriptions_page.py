import streamlit as st
import hmac
import hashlib
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from utils.db import get_supabase, require_user
from subscriptions.utils import plan_name, format_inr


# ---------------------------------------------------------
# PAYMENT SUCCESS HANDLER
# ---------------------------------------------------------
def handle_payment_success() -> None:
    """
    Handles Razorpay redirect:
    ?page=subscriptions&payment_id=xxx&order_id=xxx&signature=xxx
    """

    params = st.query_params

    payment_id = params.get("payment_id", [""])[0]
    order_id = params.get("order_id", [""])[0]
    signature = params.get("signature", [""])[0]

    if not payment_id or not order_id or not signature:
        st.info("No payment information found.")
        return

    # ---------------------------------------------------------
    # Verify Razorpay signature
    # ---------------------------------------------------------
    from utils.razorpay import get_razorpay_keys
    key_id, key_secret = get_razorpay_keys()

    generated_signature = hmac.new(
        key_secret.encode(),
        f"{order_id}|{payment_id}".encode(),
        hashlib.sha256
    ).hexdigest()

    if generated_signature != signature:
        st.error("Payment verification failed. Signature mismatch.")
        return

    # ---------------------------------------------------------
    # Fetch subscription by order_id
    # ---------------------------------------------------------
    sb = get_supabase()

    res = (
        sb.table("subscriptions")
        .select("*")
        .eq("razorpay_order_id", order_id)
        .single()
        .execute()
    )

    sub: Optional[Dict[str, Any]] = res.data if isinstance(res.data, dict) else None
    if not sub:
        st.error("Subscription not found for this payment.")
        return

    sub_id = sub.get("id")
    plan_code = sub.get("plan_code", "")

    # ---------------------------------------------------------
    # Compute subscription duration
    # ---------------------------------------------------------
    if plan_code == "MTH99":
        duration = timedelta(days=30)
    elif plan_code == "YR999":
        duration = timedelta(days=365)
    else:
        duration = timedelta(days=30)

    now = datetime.utcnow()
    expires = now + duration

    # ---------------------------------------------------------
    # Update subscription → ACTIVE
    # ---------------------------------------------------------
    sb.table("subscriptions").update({
        "status": "active",
        "razorpay_payment_id": payment_id,
        "started_at": now.isoformat(),
        "expires_at": expires.isoformat(),
    }).eq("id", sub_id).execute()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # Handle Razorpay redirect FIRST
    # ---------------------------------------------------------
    params = st.query_params
    if "payment_id" in params:
        handle_payment_success()
        return

    # ---------------------------------------------------------
    # Require logged-in user
    # ---------------------------------------------------------
    user_dict = require_user()
    user_id = str(user_dict.get("id", ""))

    sb = get_supabase()

    # ---------------------------------------------------------
    # Fetch active subscription
    # ---------------------------------------------------------
    res = (
        sb.table("subscriptions")
        .select("*")
        .eq("user_id", user_id)
        .single()
        .execute()
    )

    sub: Optional[Dict[str, Any]] = res.data if isinstance(res.data, dict) else None

    if sub and sub.get("status") == "active":
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
    else:
        st.warning("You do not have an active subscription.")

    # ---------------------------------------------------------
    # Plan selection
    # ---------------------------------------------------------
    st.subheader("Choose a Plan")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Buy Monthly"):
            _start_checkout(sb, user_id, "MTH99", 9900)

    with col2:
        if st.button("Buy Yearly"):
            _start_checkout(sb, user_id, "YR999", 99900)


# ---------------------------------------------------------
# START CHECKOUT (UPSERT + REDIRECT)
# ---------------------------------------------------------
def _start_checkout(sb, user_id: str, plan_code: str, amount_paise: int) -> None:
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
                on_conflict="user_id"
            )
            .execute()
        )
    except Exception as exc:
        st.error(f"Failed to start checkout. ({exc})")
        return

    sub = res.data[0] if isinstance(res.data, list) and res.data else None
    if not sub:
        st.error("Failed to create subscription record.")
        return

    sub_id = sub.get("id")

    # Redirect to Razorpay checkout page
    st.query_params = {
        "page": "razorpay_checkout",
        "sub_id": str(sub_id),
    }
    st.rerun()
