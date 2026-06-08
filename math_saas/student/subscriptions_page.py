# math_saas/student/subscriptions_page.py

import datetime as dt
import streamlit as st
from typing import Any, Dict

from math_saas.subscriptions.core import (
    create_subscription,
    activate_subscription,
    get_latest_subscription,
)
from math_saas.subscriptions.plans import PLANS
from math_saas.utils.payment import create_order, verify_payment_signature


# ---------------------------------------------------------
# HANDLE PAYMENT CALLBACK
# ---------------------------------------------------------
def _handle_payment_callback(user_id: str) -> None:
    params = st.query_params

    order_id = params.get("order_id")
    payment_id = params.get("payment_id")
    signature = params.get("signature")

    if not (order_id and payment_id and signature):
        return

    if not verify_payment_signature(order_id, payment_id, signature):
        st.error("Payment verification failed.")
        return

    activate_subscription(order_id, payment_id, signature)

    st.success("Payment successful! Subscription activated.")
    st.rerun()


# ---------------------------------------------------------
# FREE PLAN ACTIVATION
# ---------------------------------------------------------
def _activate_free_plan(user_id: str, plan_code: str) -> None:
    create_subscription(
        user_id=user_id,
        plan_code=plan_code,
        status="active",
        amount=0,
        currency="INR",
    )
    st.success("Free plan activated!")
    st.rerun()


# ---------------------------------------------------------
# PAID PLAN FLOW
# ---------------------------------------------------------
def _start_paid_flow(user_id: str, plan_code: str, plan: Dict[str, Any]) -> None:
    price = int(plan["price_inr"])
    amount_in_paise = price * 100

    receipt = f"{user_id}-{plan_code}-{int(dt.datetime.utcnow().timestamp())}"

    order = create_order(
        amount_in_paise=amount_in_paise,
        receipt=receipt,
        notes={"user_id": str(user_id), "plan_code": str(plan_code)},
    )

    # Create pending subscription
    create_subscription(
        user_id=user_id,
        plan_code=plan_code,
        status="pending",
        amount=amount_in_paise,
        currency="INR",
        razorpay_order_id=order["id"],
    )

    _render_razorpay_checkout(order, plan)


# ---------------------------------------------------------
# RAZORPAY CHECKOUT UI
# ---------------------------------------------------------
def _render_razorpay_checkout(order: Dict[str, Any], plan: Dict[str, Any]) -> None:
    from math_saas.config import RAZORPAY_KEY_ID

    html = f"""
    <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
    <script>
      var options = {{
          "key": "{RAZORPAY_KEY_ID}",
          "amount": {order['amount']},
          "currency": "INR",
          "name": "Math Hub",
          "description": "{plan['name']}",
          "order_id": "{order['id']}",
          "handler": function (response) {{
              const params = new URLSearchParams({{
                  "order_id": response.razorpay_order_id,
                  "payment_id": response.razorpay_payment_id,
                  "signature": response.razorpay_signature
              }});
              window.location.search = params.toString();
          }},
          "theme": {{
              "color": "#00ff88"
          }}
      }};
      var rzp1 = new Razorpay(options);
      rzp1.open();
    </script>
    """
    st.markdown(html, unsafe_allow_html=True)


# ---------------------------------------------------------
# MAIN PAGE
# ---------------------------------------------------------
def render_subscriptions_page() -> None:
    st.header("Your Subscription")

    student = st.session_state.get("student")
    if not student:
        st.error("Please login as student.")
        return

    user_id: str = student["id"]

    # Handle Razorpay callback
    _handle_payment_callback(user_id)

    # Fetch latest subscription
    current = get_latest_subscription(user_id)

    # Display current subscription
    if current and current.get("status") == "active":
        st.success(
            f"Active plan: {current.get('plan_code')} "
            f"(expires at {current.get('expires_at')})"
        )
    else:
        st.info("No active subscription.")

    st.subheader("Choose a Plan")

    cols = st.columns(3)
    plan_codes = ["FREE", "MONTHLY", "ANNUAL"]

    for col, code in zip(cols, plan_codes):
        if code not in PLANS:
            continue

        plan = PLANS[code]

        with col:
            st.markdown(f"### {plan['name']}")
            st.write(f"Price: ₹{plan['price_inr']}")
            st.write(f"Duration: {plan['duration_days']} days")

            if st.button(f"Select {plan['name']}", key=f"plan_{code}"):
                if code == "FREE":
                    _activate_free_plan(user_id, code)
                else:
                    _start_paid_flow(user_id, code, plan)
