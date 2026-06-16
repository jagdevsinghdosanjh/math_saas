import streamlit as st
import streamlit.components.v1 as components   # <-- FIXED

from math_saas.subscriptions.payment_callback import handle_payment_callback
from math_saas.subscriptions.core import create_subscription_order
from math_saas.student.dashboard import get_user_active_subscription
import os


def render_subscriptions_page():
    st.markdown("<h3>Subscription</h3>", unsafe_allow_html=True)

    student = st.session_state.get("student")
    if not isinstance(student, dict):
        st.error("Please login as student.")
        return

    user_id = str(student.get("id") or "")
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

    plan = sub.get("plan_code", "Unknown")
    expires = sub.get("expires_at", "Unknown")

    st.success("You have an active subscription.")
    st.write(f"**Plan:** {plan}")
    st.write(f"**Expires:** {expires}")


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

            launch_razorpay_checkout(
                order_id=order["order_id"],
                amount=order["amount"],
                user_email=user_email,
            )
            st.stop()


def launch_razorpay_checkout(order_id: str, amount: int, user_email: str):
    key_id = os.getenv("RAZORPAY_KEY_ID")

    checkout_html = f"""
    <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
    <script>
        var options = {{
            "key": "{key_id}",
            "amount": "{amount}",
            "currency": "INR",
            "name": "Math Hub",
            "description": "Subscription Payment",
            "order_id": "{order_id}",
            "handler": function (response) {{
                window.location.href = "?order_id=" + response.razorpay_order_id
                    + "&payment_id=" + response.razorpay_payment_id
                    + "&signature=" + response.razorpay_signature;
            }},
            "prefill": {{
                "email": "{user_email}"
            }},
            "theme": {{
                "color": "#00ff88"
            }}
        }};
        var rzp = new Razorpay(options);
        rzp.open();
    </script>
    """

    # components.html(checkout_html, height=50)   # <-- FIXED
    components.html(checkout_html, width=850,height=600, scrolling=True)



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
            st.session_state.pop("checkout_mode", None)
            st.query_params.clear()
            st.rerun()
        else:
            st.error(result["error"])
