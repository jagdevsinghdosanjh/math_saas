import streamlit as st

from math_saas.subscriptions.payment_callback import handle_payment_callback
from math_saas.subscriptions.core import create_subscription_order
from math_saas.student.dashboard import get_user_active_subscription


def render_subscriptions_page():
    st.markdown("<h3>Subscription</h3>", unsafe_allow_html=True)

    student = st.session_state.get("student")
    if not isinstance(student, dict):
        st.error("Please login as student.")
        return

    user_id = str(student.get("id") or "")

    # Handle Razorpay callback (if present)
    _handle_payment_query_params()

    # Check active subscription
    sub = get_user_active_subscription(user_id)

    if sub is None:
        st.info("You do not have an active subscription.")

        if st.button("Buy Subscription"):
            st.session_state["checkout_mode"] = True
            st.rerun()

        if st.session_state.get("checkout_mode"):
            render_checkout_page(user_id)

        return

    plan = sub.get("plan_code", "Unknown")
    expires = sub.get("expires_at", "Unknown")

    st.success("You have an active subscription.")
    st.write(f"**Plan:** {plan}")
    st.write(f"**Expires:** {expires}")


def render_checkout_page(user_id: str):
    st.subheader("Choose a Plan")

    plans = [
        {"name": "Monthly", "plan_code": "MONTHLY"},
        {"name": "Annual", "plan_code": "ANNUAL"},
    ]

    for p in plans:
        if st.button(f"Buy {p['name']}", key=f"plan_{p['plan_code']}"):
            order = create_subscription_order(user_id, p["plan_code"])
            if not order:
                st.error("Failed to create order.")
                return

            order_id = order["order_id"]

            # Redirect to Razorpay Checkout page (hosted)
            # You can also embed Razorpay Checkout.js if you prefer
            st.markdown(
                f"""
                <script>
                    window.location.href = "https://checkout.razorpay.com/v1/checkout.js?order_id={order_id}";
                </script>
                """,
                unsafe_allow_html=True,
            )
            st.stop()


def _handle_payment_query_params():
    params = st.query_params

    if "order_id" in params and "payment_id" in params and "signature" in params:
        result = handle_payment_callback(
            params["order_id"],
            params["payment_id"],
            params["signature"],
        )

        if result["success"]:
            st.success("Payment successful! Subscription activated.")
            # Clear checkout mode and query params
            if "checkout_mode" in st.session_state:
                del st.session_state["checkout_mode"]
            st.query_params.clear()
            st.rerun()
        else:
            st.error(result["error"])
