import streamlit as st
import hmac
import hashlib
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from utils.db import get_supabase, require_user
from subscriptions.utils import plan_name, format_inr


# ---------------------------------------------------------
# SAFE HELPERS
# ---------------------------------------------------------
def _safe_dict(value: Any) -> Optional[Dict[str, Any]]:
    return value if isinstance(value, dict) else None


# ---------------------------------------------------------
# PAYMENT SUCCESS HANDLER
# ---------------------------------------------------------
def handle_payment_success() -> None:
    st.write("DEBUG: handle_payment_success() called")

    params = st.query_params
    st.write("DEBUG: query_params =", params)

    payment_id = params.get("payment_id", [""])[0]
    order_id = params.get("order_id", [""])[0]
    signature = params.get("signature", [""])[0]

    st.write("DEBUG: payment_id =", payment_id)
    st.write("DEBUG: order_id =", order_id)
    st.write("DEBUG: signature =", signature)

    if not payment_id or not order_id or not signature:
        st.info("No payment information found.")
        return

    from utils.razorpay import get_razorpay_keys
    _, key_secret = get_razorpay_keys()

    generated_signature = hmac.new(
        key_secret.encode(),
        f"{order_id}|{payment_id}".encode(),
        hashlib.sha256,
    ).hexdigest()

    st.write("DEBUG: generated_signature =", generated_signature)

    if generated_signature != signature:
        st.error("Payment verification failed. Signature mismatch.")
        return

    sb = get_supabase()
    st.write("DEBUG: got Supabase client in handle_payment_success")

    res = (
        sb.table("subscriptions")
        .select("*")
        .eq("razorpay_order_id", order_id)
        .maybe_single()
        .execute()
    )

    st.write("DEBUG: Supabase response for payment success =", res)

    sub = _safe_dict(res.data if res else None)
    st.write("DEBUG: subscription record from payment success =", sub)

    if not sub:
        st.error("Subscription not found for this payment.")
        return

    sub_id = sub.get("id")
    plan_code = sub.get("plan_code", "")

    st.write("DEBUG: sub_id =", sub_id)
    st.write("DEBUG: plan_code =", plan_code)

    duration_days = 30 if plan_code == "MTH99" else 365
    now = datetime.utcnow()
    expires = now + timedelta(days=duration_days)

    sb.table("subscriptions").update(
        {
            "status": "active",
            "razorpay_payment_id": payment_id,
            "started_at": now.isoformat(),
            "expires_at": expires.isoformat(),
        }
    ).eq("id", sub_id).execute()

    st.write("DEBUG: subscription updated to active")

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
    st.write("DEBUG: render_subscriptions_page() called")

    # Handle payment callback
    params = st.query_params
    st.write("DEBUG: query_params at subscriptions page =", params)

    if "payment_id" in params:
        st.write("DEBUG: payment_id found in query_params, calling handle_payment_success()")
        handle_payment_success()
        return

    user_dict = require_user()
    user_id = str(user_dict.get("id", ""))

    st.write("DEBUG: user_dict =", user_dict)
    st.write("DEBUG: user_id =", user_id)

    sb = get_supabase()
    st.write("DEBUG: got Supabase client in render_subscriptions_page")

    res = (
        sb.table("subscriptions")
        .select("*")
        .eq("user_id", user_id)
        .maybe_single()
        .execute()
    )

    st.write("DEBUG: Supabase response for user subscription =", res)

    sub = _safe_dict(res.data if res else None)
    st.write("DEBUG: subscription record for user =", sub)

    if not sub:
        st.warning("You do not have any subscription yet.")
        _render_plan_selection(sb, user_id)
        return

    if sub.get("status") != "active":
        st.warning("You do not have an active subscription.")
        _render_plan_selection(sb, user_id)
        return

    plan = plan_name(sub.get("plan_code", ""))
    amount = format_inr(sub.get("amount", 0))
    started = sub.get("started_at", "")
    expires = sub.get("expires_at", "")

    st.write("DEBUG: active subscription details:", {
        "plan": plan,
        "amount": amount,
        "started": started,
        "expires": expires,
    })

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
    st.write("DEBUG: _render_plan_selection() called for user_id =", user_id)

    st.subheader("Choose a Plan")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Buy Monthly"):
            st.write("DEBUG: Buy Monthly button clicked")
            _start_checkout(sb, user_id, "MTH99", 9900)

    with col2:
        if st.button("Buy Yearly"):
            st.write("DEBUG: Buy Yearly button clicked")
            _start_checkout(sb, user_id, "YR999", 99900)


# ---------------------------------------------------------
# START CHECKOUT (UPSERT + NAVIGATE)
# ---------------------------------------------------------
def _start_checkout(sb: Any, user_id: str, plan_code: str, amount_paise: int) -> None:
    st.write("DEBUG: _start_checkout() called with:", {
        "user_id": user_id,
        "plan_code": plan_code,
        "amount_paise": amount_paise,
    })

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
        st.write("DEBUG: Exception in _start_checkout:", exc)
        return

    st.write("DEBUG: Supabase upsert response in _start_checkout =", res)

    data = res.data if res else None
    sub_list = data if isinstance(data, list) else []
    sub = sub_list[0] if sub_list else None

    st.write("DEBUG: sub_list =", sub_list)
    st.write("DEBUG: sub =", sub)

    if not isinstance(sub, dict):
        st.error("Failed to create subscription record.")
        return

    sub_id = sub.get("id")
    st.write("DEBUG: Checkout started, sub_id =", sub_id)

    # Store subscription ID for checkout page
    st.session_state["sub_id"] = str(sub_id)
    st.write("DEBUG: st.session_state['sub_id'] set to", st.session_state.get("sub_id"))

    # Navigate to Razorpay checkout page
    st.write("DEBUG: switching page to pages/razorpay_checkout.py")
    st.switch_page("pages/razorpay_checkout.py")
