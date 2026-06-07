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


# -----------------------------
# PAYMENT CALLBACK HANDLER
# -----------------------------
def _handle_payment_callback(user_id: str):
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
    st.query_params.clear()
    st.rerun()


# -----------------------------
# FREE PLAN ACTIVATION
# -----------------------------
def _activate_free_plan(user_id: str, plan_code: str):
    create_subscription(
        user_id=user_id,
        plan_code=plan_code,
        status="active",
        amount=0,
        currency="INR",
    )
    st.success("Free plan activated!")
    st.rerun()


# -----------------------------
# PAID PLAN FLOW
# -----------------------------
def _start_paid_flow(user_id: str, plan_code: str, plan: Dict[str, Any]):
    amount_in_paise = plan["price_inr"] * 100
    receipt = f"{user_id}-{plan_code}-{int(dt.datetime.utcnow().timestamp())}"

    order = create_order(
        amount_in_paise=amount_in_paise,
        receipt=receipt,
        notes={"user_id": user_id, "plan_code": plan_code},
    )

    create_subscription(
        user_id=user_id,
        plan_code=plan_code,
        status="pending",
        amount=amount_in_paise,
        currency="INR",
        razorpay_order_id=order["id"],
    )

    _render_razorpay_checkout(order, plan)


# -----------------------------
# RAZORPAY CHECKOUT UI
# -----------------------------
def _render_razorpay_checkout(order: Dict[str, Any], plan: Dict[str, Any]):
    from math_saas.config import RAZORPAY_KEY_ID

    html = f"""
    <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
    <script>
      var options = {{
          "key": "{RAZORPAY_KEY_ID}",
          "amount": "{order['amount']}",
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


# -----------------------------
# MAIN PAGE
# -----------------------------
def render_subscriptions_page():
    st.header("Your Subscription")

    student = st.session_state.get("student")
    if not student:
        st.error("Please login as student.")
        return

    user_id = student["id"]

    _handle_payment_callback(user_id)

    current = get_latest_subscription(user_id)

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

# import datetime as dt
# import streamlit as st
# from typing import Any, Dict, List, Optional

# from math_saas.utils.db import get_supabase
# from math_saas.subscriptions.plans import PLANS
# from math_saas.utils.payment import create_order


# # -----------------------------
# # Helper: Fetch latest subscription
# # -----------------------------
# def _get_latest_subscription(user_id: str) -> Optional[Dict[str, Any]]:
#     sb = get_supabase()

#     res = (
#         sb.table("subscriptions")
#         .select("*")
#         .eq("user_id", user_id)
#         .order("expires_at", desc=True)
#         .limit(1)
#         .execute()
#     )

#     raw = res.data or []

#     # Pylance-safe filtering
#     data: List[Dict[str, Any]] = [
#         item for item in raw if isinstance(item, dict)
#     ]

#     return data[0] if data else None


# # -----------------------------
# # FREE PLAN ACTIVATION
# # -----------------------------
# def _activate_free_plan(user_id: str, plan_code: str):
#     sb = get_supabase()

#     now = dt.datetime.utcnow()
#     expires = now + dt.timedelta(days=PLANS[plan_code]["duration_days"])

#     sb.table("subscriptions").insert(
#         {
#             "user_id": user_id,
#             "plan_code": plan_code,
#             "status": "active",
#             "amount": 0,
#             "currency": "INR",
#             "started_at": now.isoformat(),
#             "expires_at": expires.isoformat(),
#         }
#     ).execute()

#     st.success("Free plan activated!")
#     st.rerun()


# # -----------------------------
# # PAID PLAN FLOW (ORDER CREATION)
# # -----------------------------
# def _start_paid_flow(user_id: str, plan_code: str, plan: Dict[str, Any]):
#     sb = get_supabase()

#     amount_in_paise = plan["price_inr"] * 100
#     receipt = f"{user_id}-{plan_code}-{int(dt.datetime.utcnow().timestamp())}"

#     order = create_order(
#         amount_in_paise=amount_in_paise,
#         receipt=receipt,
#         notes={"user_id": user_id, "plan_code": plan_code},
#     )

#     now = dt.datetime.utcnow()
#     expires = now + dt.timedelta(days=plan["duration_days"])

#     sb.table("subscriptions").insert(
#         {
#             "user_id": user_id,
#             "plan_code": plan_code,
#             "status": "pending",
#             "amount": amount_in_paise,
#             "currency": "INR",
#             "started_at": now.isoformat(),
#             "expires_at": expires.isoformat(),
#             "razorpay_order_id": order["id"],
#         }
#     ).execute()

#     st.info("Redirecting to Razorpay Checkout...")

#     _render_razorpay_checkout(order, plan)


# # -----------------------------
# # RAZORPAY CHECKOUT UI
# # -----------------------------
# def _render_razorpay_checkout(order: Dict[str, Any], plan: Dict[str, Any]):
#     from math_saas.config import RAZORPAY_KEY_ID

#     html = f"""
#     <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
#     <script>
#       var options = {{
#           "key": "{RAZORPAY_KEY_ID}",
#           "amount": "{order['amount']}",
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


# # -----------------------------
# # PAYMENT CALLBACK HANDLER
# # -----------------------------
# def _handle_payment_callback(user_id: str):
#     params = st.query_params

#     order_id = params.get("order_id")
#     payment_id = params.get("payment_id")
#     signature = params.get("signature")

#     if not (order_id and payment_id and signature):
#         return  # No callback present

#     from math_saas.utils.payment import verify_payment_signature

#     if not verify_payment_signature(order_id, payment_id, signature):
#         st.error("Payment verification failed.")
#         return

#     sb = get_supabase()

#     sb.table("subscriptions").update(
#         {
#             "status": "active",
#             "razorpay_payment_id": payment_id,
#             "razorpay_signature": signature,
#         }
#     ).eq("user_id", user_id).eq("razorpay_order_id", order_id).execute()

#     st.success("Payment successful! Subscription activated.")

#     # Clear query params to avoid reprocessing
#     st.query_params.clear()
#     st.rerun()


# # -----------------------------
# # MAIN PAGE
# # -----------------------------
# def render_subscriptions_page():
#     st.header("Your Subscription")

#     student = st.session_state.get("student")
#     if not student:
#         st.error("Please login as student.")
#         return

#     user_id = student["id"]

#     # Improvement 1: Handle Razorpay callback
#     _handle_payment_callback(user_id)

#     # Fetch latest subscription safely
#     current = _get_latest_subscription(user_id)

#     if current and current.get("status") == "active":
#         st.success(
#             f"Active plan: {current.get('plan_code')} "
#             f"(expires at {current.get('expires_at')})"
#         )
#     else:
#         st.info("No active subscription.")

#     st.subheader("Choose a Plan")

#     cols = st.columns(3)
#     plan_codes = ["FREE", "MONTHLY", "ANNUAL"]

#     for col, code in zip(cols, plan_codes):

#         # Improvement 2: Guard against missing plan codes
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
