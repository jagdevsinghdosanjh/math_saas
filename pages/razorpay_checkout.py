# pages/razorpay_checkout.py

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Razorpay Checkout", page_icon="💳", layout="centered")

st.title("Complete Your Subscription Payment")

# ---- 1. Read data from session_state ----
order_id = st.session_state.get("razorpay_order_id")
amount = st.session_state.get("razorpay_amount")      # in paise (e.g. 49900)
key_id = st.session_state.get("razorpay_key_id")      # Razorpay key_id
user_id = st.session_state.get("user_id")             # optional, for your own tracking

if not order_id or not amount or not key_id:
    st.error("Missing payment details. Please go back and start the subscription again.")
    st.stop()

st.info(f"Order ID: `{order_id}` — Amount: ₹{amount/100:.2f}")

# ---- 2. Build the Razorpay Checkout HTML/JS safely ----
callback_url = st.secrets["app"]["base_url"]  # e.g. "https://math-saas.streamlit.app"

html_code = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <title>Razorpay Checkout</title>
  <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
</head>
<body>
  <button id="rzp-button" style="
      padding: 12px 24px;
      background-color: #10b981;
      color: white;
      border: none;
      border-radius: 6px;
      font-size: 16px;
      cursor: pointer;
  ">
    Pay Now
  </button>

  <script>
    var options = {{
        "key": "{key_id}",
        "amount": "{amount}",
        "currency": "INR",
        "name": "Math Hub",
        "description": "Subscription Payment",
        "order_id": "{order_id}",
        "handler": function (response) {{
            var url = "{callback_url}" +
                      "?order_id={order_id}" +
                      "&payment_id=" + encodeURIComponent(response.razorpay_payment_id) +
                      "&signature=" + encodeURIComponent(response.razorpay_signature);
            window.location.href = url;
        }},
        "prefill": {{
            "name": "",
            "email": "",
            "contact": ""
        }},
        "theme": {{
            "color": "#10b981"
        }}
    }};

    var rzp1 = new Razorpay(options);
    document.getElementById('rzp-button').onclick = function(e) {{
        rzp1.open();
        e.preventDefault();
    }};
  </script>
</body>
</html>
"""

components.html(html_code, width=900, height=800)

# import streamlit as st
# import os

# st.set_page_config(page_title="Processing Payment...", layout="centered")

# def main():
#     order_id = st.query_params.get("order_id", None)
#     amount = st.query_params.get("amount", None)
#     email = st.query_params.get("email", "")

#     if not order_id or not amount:
#         st.error("Missing order details.")
#         return

#     key_id = os.getenv("RAZORPAY_KEY_ID")

#     st.markdown("### Redirecting to Razorpay…")

#     html = f"""
#     <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
#     <script>
#         var options = {{
#             "key": "{key_id}",
#             "amount": "{amount}",
#             "currency": "INR",
#             "name": "Math Hub",
#             "description": "Subscription Payment",
#             "order_id": "{order_id}",

#             "handler": function (response) {{
#                 window.location.href =
#                     "/?order_id={order_id}"
#                     + "&payment_id=" + response.razorpay_payment_id
#                     + "&signature=" + response.razorpay_signature;
#             }},

#             "prefill": {{
#                 "email": "{email}"
#             }},
#             "theme": {{
#                 "color": "#00ff88"
#             }}
#         }};

#         var rzp = new Razorpay(options);
#         rzp.open();
#     </script>
#     """

#     st.markdown(html, unsafe_allow_html=True)

# main()