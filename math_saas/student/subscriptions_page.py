# math_saas/student/subscriptions_page.py

import datetime as dt
import streamlit as st
from typing import Any, Dict, Optional

from math_saas.subscriptions.core import (
    create_subscription,
    activate_subscription,
    get_latest_subscription, #noqa  # kept for compatibility
    get_active_subscription,   # now exported in core.py
)
from math_saas.subscriptions.plans import PLANS
from math_saas.utils.payment import create_order, verify_payment_signature
from math_saas.auth import TEXT_MUTED


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
    active = get_active_subscription(user_id)
    if active:
        st.info("You already have an active subscription.")
        return

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
    price_raw = plan.get("price_inr", 0)
    try:
        price = int(price_raw)
    except Exception:
        st.error("Invalid plan price.")
        return

    amount_in_paise = price * 100
    receipt = f"{user_id}-{plan_code}-{int(dt.datetime.utcnow().timestamp())}"

    try:
        order = create_order(
            amount_in_paise=amount_in_paise,
            receipt=receipt,
            notes={"user_id": str(user_id), "plan_code": str(plan_code)},
        )
    except Exception as e:
        st.error(f"Failed to create payment order: {e}")
        return

    create_subscription(
        user_id=user_id,
        plan_code=plan_code,
        status="pending",
        amount=amount_in_paise,
        currency="INR",
        razorpay_order_id=order.get("id"),
    )

    _render_razorpay_checkout(order, plan)


# ---------------------------------------------------------
# RAZORPAY CHECKOUT UI
# ---------------------------------------------------------
def _render_razorpay_checkout(order: Dict[str, Any], plan: Dict[str, Any]) -> None:
    from math_saas.config import RAZORPAY_KEY_ID

    order_id = str(order.get("id", ""))
    amount = int(order.get("amount", 0))
    plan_name = str(plan.get("name", "Math Hub Plan"))

    html = f"""
    <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
    <script>
      var options = {{
          "key": "{RAZORPAY_KEY_ID}",
          "amount": {amount},
          "currency": "INR",
          "name": "Math Hub",
          "description": "{plan_name}",
          "order_id": "{order_id}",
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

    student_raw = st.session_state.get("student")
    if not isinstance(student_raw, dict):
        st.error("Please login as student.")
        return

    raw_id: Optional[Any] = student_raw.get("id")
    user_id = str(raw_id) if raw_id is not None else ""

    if not user_id:
        st.error("Invalid student session.")
        return

    _handle_payment_callback(user_id)

    current = get_active_subscription(user_id)

    if current:
        plan_code = str(current.get("plan_code", ""))
        expires = str(current.get("expires_at", ""))

        st.markdown(
            f"""
            <div class="neon-card" style="margin-bottom:16px;">
                <h4>Active Plan: {plan_code}</h4>
                <p style="color:{TEXT_MUTED};">
                    Expires at: {expires}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("No active subscription.")

    st.subheader("Choose a Plan")

    cols = st.columns(3)
    plan_codes = ["FREE", "MONTHLY", "ANNUAL"]

    for col, code in zip(cols, plan_codes):
        plan = PLANS.get(code)
        if not isinstance(plan, dict):
            continue

        name = str(plan.get("name", code))
        price = str(plan.get("price_inr", "0"))
        duration = str(plan.get("duration_days", "0"))

        with col:
            st.markdown(f"### {name}")
            st.write(f"Price: ₹{price}")
            st.write(f"Duration: {duration} days")

            if st.button(f"Select {name}", key=f"plan_{code}"):
                if code == "FREE":
                    _activate_free_plan(user_id, code)
                else:
                    _start_paid_flow(user_id, code, plan)

# import datetime as dt
# import streamlit as st
# from typing import Any, Dict

# from math_saas.subscriptions.core import (
#     create_subscription,
#     activate_subscription,
#     get_active_subscription,
# )
# from math_saas.subscriptions.plans import PLANS
# from math_saas.utils.payment import create_order, verify_payment_signature
# from math_saas.auth import TEXT_MUTED


# # ---------------------------------------------------------
# # HANDLE PAYMENT CALLBACK
# # ---------------------------------------------------------
# def _handle_payment_callback(user_id: str) -> None:
#     params = st.query_params

#     order_id = params.get("order_id")
#     payment_id = params.get("payment_id")
#     signature = params.get("signature")

#     if not (order_id and payment_id and signature):
#         return

#     if not verify_payment_signature(order_id, payment_id, signature):
#         st.error("Payment verification failed.")
#         return

#     activate_subscription(order_id, payment_id, signature)

#     st.success("Payment successful! Subscription activated.")
#     st.rerun()


# # ---------------------------------------------------------
# # FREE PLAN ACTIVATION
# # ---------------------------------------------------------
# def _activate_free_plan(user_id: str, plan_code: str) -> None:
#     # Prevent duplicate free activations
#     active = get_active_subscription(user_id)
#     if active:
#         st.info("You already have an active subscription.")
#         return

#     create_subscription(
#         user_id=user_id,
#         plan_code=plan_code,
#         status="active",
#         amount=0,
#         currency="INR",
#     )
#     st.success("Free plan activated!")
#     st.rerun()


# # ---------------------------------------------------------
# # PAID PLAN FLOW
# # ---------------------------------------------------------
# def _start_paid_flow(user_id: str, plan_code: str, plan: Dict[str, Any]) -> None:
#     try:
#         price = int(plan.get("price_inr", 0))
#     except Exception:
#         st.error("Invalid plan price.")
#         return

#     amount_in_paise = price * 100
#     receipt = f"{user_id}-{plan_code}-{int(dt.datetime.utcnow().timestamp())}"

#     # Create Razorpay order
#     try:
#         order = create_order(
#             amount_in_paise=amount_in_paise,
#             receipt=receipt,
#             notes={"user_id": str(user_id), "plan_code": str(plan_code)},
#         )
#     except Exception as e:
#         st.error(f"Failed to create payment order: {e}")
#         return

#     # Create pending subscription
#     create_subscription(
#         user_id=user_id,
#         plan_code=plan_code,
#         status="pending",
#         amount=amount_in_paise,
#         currency="INR",
#         razorpay_order_id=order["id"],
#     )

#     _render_razorpay_checkout(order, plan)


# # ---------------------------------------------------------
# # RAZORPAY CHECKOUT UI
# # ---------------------------------------------------------
# def _render_razorpay_checkout(order: Dict[str, Any], plan: Dict[str, Any]) -> None:
#     from math_saas.config import RAZORPAY_KEY_ID

#     html = f"""
#     <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
#     <script>
#       var options = {{
#           "key": "{RAZORPAY_KEY_ID}",
#           "amount": {order['amount']},
#           "currency": "INR",
#           "name": "Math Hub",
#           "description": "{plan['name']}",
#           "order_id": "{order['id']}",
#           "handler": function (response) {{
#               const params = new URLSearchParams({{
#                   "order_id": response.razorpay_order_id,
#                   "payment_id": response.razorpay_payment_id,
#                   "signature": response.razorpay_signature
#               }});
#               window.location.search = params.toString();
#           }},
#           "theme": {{
#               "color": "#00ff88"
#           }}
#       }};
#       var rzp1 = new Razorpay(options);
#       rzp1.open();
#     </script>
#     """
#     st.markdown(html, unsafe_allow_html=True)


# # ---------------------------------------------------------
# # MAIN PAGE
# # ---------------------------------------------------------
# def render_subscriptions_page() -> None:
#     st.header("Your Subscription")

#     student = st.session_state.get("student")
#     if not isinstance(student, dict):
#         st.error("Please login as student.")
#         return

#     user_id: str = student.get("id")
#     if not user_id:
#         st.error("Invalid student session.")
#         return

#     # Handle Razorpay callback
#     _handle_payment_callback(user_id)

#     # Fetch active subscription
#     current = get_active_subscription(user_id)

#     # Display current subscription
#     if current:
#         st.markdown(
#             f"""
#             <div class="neon-card" style="margin-bottom:16px;">
#                 <h4>Active Plan: {current.get('plan_code')}</h4>
#                 <p style="color:{TEXT_MUTED};">
#                     Expires at: {current.get('expires_at')}
#                 </p>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )
#     else:
#         st.info("No active subscription.")

#     st.subheader("Choose a Plan")

#     cols = st.columns(3)
#     plan_codes = ["FREE", "MONTHLY", "ANNUAL"]

#     for col, code in zip(cols, plan_codes):
#         if code not in PLANS:
#             continue

#         plan = PLANS[code]

#         with col:
#             st.markdown(f"### {plan['name']}")
#             st.write(f"Price: ₹{plan['price_inr']}")
#             st.write(f"Duration: {plan['duration_days']} days")

#             if st.button(f"Select {plan['name']}", key=f"plan_{code}"):
#                 if code == "FREE":
#                     _activate_free_plan(user_id, code)
#                 else:
#                     _start_paid_flow(user_id, code, plan)
