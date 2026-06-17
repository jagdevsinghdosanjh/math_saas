import streamlit as st
from subscriptions.payment_callback import handle_payment_callback
from subscriptions.core import create_subscription_order
from student.dashboard import get_user_active_subscription

def render_subscriptions_page():
    st.markdown("<h3>Subscription</h3>", unsafe_allow_html=True)

    student = st.session_state.get("student")
    if not isinstance(student, dict):
        st.error("Please login as student.")
        return

    user_id = str(student["id"])
    user_email = student.get("email", "")

    _handle_payment_query_params()

    sub = get_user_active_subscription(user_id)

    if sub is None:
        st.info("You do not have an active subscription.")

        if st.button("Buy Subscription"):
            st.session_state["checkout_mode"] = True
            st.rerun()

        if st.session_state.get("checkout_mode"):
            render_checkout_page(user_id, user_email)

        return

    st.success("You have an active subscription.")
    st.write(f"**Plan:** {sub.get('plan')}")
    st.write(f"**Expires:** {sub.get('expires_at')}")


def render_checkout_page(user_id: str, user_email: str):
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

            st.query_params.update({
                "order_id": order["order_id"],
                "amount": order["amount"],
                "email": user_email
            })
            st.switch_page()

            st.switch_page('razorpay_checkout')


def _handle_payment_query_params():
    params = st.query_params

    if {"order_id", "payment_id", "signature"} <= params.keys():
        result = handle_payment_callback(
            params["order_id"],
            params["payment_id"],
            params["signature"],
        )

        if result["success"]:
            st.success("Payment successful! Subscription will activate shortly.")
            st.session_state.pop("checkout_mode", None)
            st.query_params.clear()
            st.rerun()
        else:
            st.error(result["error"])
