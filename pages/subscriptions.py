import streamlit as st
import hmac
import hashlib
from datetime import datetime, timedelta

from utils.db import get_supabase
from utils.razorpay import get_razorpay_keys


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

    sub = res.data or None
    if not sub:
        st.error("Subscription not found for this payment.")
        return

    sub_id = sub["id"]
    plan_code = sub["plan_code"]

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
