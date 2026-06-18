import streamlit as st
from typing import Any, Dict, Optional

from utils.db import get_supabase
from utils.razorpay import get_razorpay_keys
from student.dashboard import get_user_active_subscription
from subscriptions.utils import format_inr, plan_name
from auth import TEXT_MUTED


# -------------------------------------------------
# MAIN PAGE
# -------------------------------------------------
def render_subscriptions_page() -> None:
    st.header("Subscription")

    student = st.session_state.get("student")
    if not isinstance(student, dict):
        st.error("Please login as student.")
        return

    user_id = str(student.get("id") or "")
    if not user_id:
        st.error("Invalid student session.")
        return

    # Razorpay keys (lazy load)
    key_id, key_secret = get_razorpay_keys()
    if not key_id or not key_secret:
        st.info("Subscription page coming soon. (Razorpay keys not configured in environment.)")
        return

    # Active subscription
    active = get_user_active_subscription(user_id)

    if active:
        plan = plan_name(str(active.get("plan_code", "")))
        amount = format_inr(active.get("amount", 0))
        status = str(active.get("status", ""))
        started = str(active.get("started_at", ""))
        expires = str(active.get("expires_at", ""))

        st.markdown(
            f"""
            <div class="neon-card" style="margin-bottom:16px;">
                <h4>{plan}</h4>
                <p style="color:{TEXT_MUTED}; margin-bottom:6px;">
                    Status: {status}<br>
                    Amount: {amount}<br>
                    Started: {started}<br>
                    Expires: {expires}<br>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.success("You have an active subscription.")
    else:
        st.warning("You do not have an active subscription.")

    # -----------------------------
    # PLAN SELECTION
    # -----------------------------
    st.subheader("Choose a Plan")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Buy Monthly"):
            _start_checkout(user_id, "MTH99", 9900)  # ₹99.00

    with col2:
        if st.button("Buy Yearly"):
            _start_checkout(user_id, "YR999", 99900)  # ₹999.00


# -------------------------------------------------
# CHECKOUT STARTER
# -------------------------------------------------
def _start_checkout(user_id: str, plan_code: str, amount_paise: int) -> None:
    sb = get_supabase()

    # Insert pending subscription
    res = (
        sb.table("subscriptions")
        .insert({
            "user_id": user_id,
            "plan": "Monthly" if plan_code == "MTH99" else "Yearly",
            "plan_code": plan_code,
            "status": "pending",
            "amount": amount_paise,
            "currency": "INR",
            "started_at": None,       # webhook will set
            "expires_at": None,       # webhook will set
            "razorpay_order_id": None # webhook will set
        })
        .execute()
    )

    data = res.data or []
    sub = data[0] if data and isinstance(data[0], dict) else None

    if not sub:
        st.error("Failed to create subscription record.")
        return

    sub_id = sub["id"]
    
    # Redirect to Razorpay checkout page
    st.query_params = {
    "page": "razorpay_checkout",
    "sub_id": str(sub_id),
    }
    st.rerun()


    # # Redirect to Razorpay checkout page
    # st.experimental_set_query_params(
    #     page="razorpay_checkout",
    #     sub_id=str(sub_id),
    # )
    # st.rerun()
