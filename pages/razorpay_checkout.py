import streamlit as st
import os

st.set_page_config(page_title="Processing Payment...", layout="centered")

def main():
    order_id = st.query_params.get("order_id", None)
    amount = st.query_params.get("amount", None)
    email = st.query_params.get("email", "")

    if not order_id or not amount:
        st.error("Missing order details.")
        return

    key_id = os.getenv("RAZORPAY_KEY_ID")

    st.markdown("### Redirecting to Razorpay…")

    html = f"""
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
                window.location.href =
                    "/?order_id={order_id}"
                    + "&payment_id=" + response.razorpay_payment_id
                    + "&signature=" + response.razorpay_signature;
            }},

            "prefill": {{
                "email": "{email}"
            }},
            "theme": {{
                "color": "#00ff88"
            }}
        }};

        var rzp = new Razorpay(options);
        rzp.open();
    </script>
    """

    st.markdown(html, unsafe_allow_html=True)

main()