import streamlit as st
from typing import Any, Dict, Optional
import streamlit.components.v1 as components

from utils.db import get_supabase
from utils.razorpay import get_razorpay_client, get_razorpay_keys
from subscriptions.utils import format_inr, plan_name


def render_razorpay_checkout() -> None:
    st.header("Razorpay Checkout")

    # Razorpay client
    client = get_razorpay_client()
    if client is None:
        st.error("Razorpay keys not configured. Cannot start checkout.")
        return

    # Read query params
    params = st.query_params
    sub_id = params.get("sub_id", [""])[0]

    if not sub_id:
        st.error("Missing subscription ID.")
        return

    # Fetch subscription
    sb = get_supabase()
    res = (
        sb.table("subscriptions")
        .select("id, user_id, amount, currency, plan, plan_code, status")
        .eq("id", sub_id)
        .single()
        .execute()
    )

    sub = res.data or {}
    if not isinstance(sub, dict):
        st.error("Subscription not found.")
        return

    raw_amount = sub.get("amount")
    amount = int(raw_amount) if isinstance(raw_amount, (int, float, str)) else 0
    currency = str(sub.get("currency") or "INR")
    user_id = str(sub.get("user_id") or "")
    plan_code = str(sub.get("plan_code") or "")
    plan = plan_name(plan_code)

    # Create Razorpay order (Pylance false error → ignore)
    order = client.order.create({  # type: ignore
        "amount": amount,
        "currency": currency,
        "payment_capture": 1,
        "notes": {
            "subscription_id": str(sub_id),
            "user_id": user_id,
            "plan_code": plan_code,
        },
    })

    order_id = str(order.get("id"))

    # Save order_id in subscriptions
    sb.table("subscriptions").update({
        "razorpay_order_id": order_id,
    }).eq("id", sub_id).execute()

    st.markdown("### Complete Payment")
    st.write(f"Plan: **{plan}**")
    st.write(f"Amount: **{format_inr(amount)}**")

    # Get Razorpay key_id safely
    key_id, _ = get_razorpay_keys()

    # ---------------------------------------------------------
    # Razorpay Checkout.js Embed (Working + Pylance-safe)
    # ---------------------------------------------------------
    checkout_html = f"""
    <html>
    <body>
    <script src="https://checkout.razorpay.com/v1/checkout.js"></script>

    <script>
        var options = {{
            "key": "{key_id}",
            "amount": "{amount}",
            "currency": "{currency}",
            "name": "Math Hub",
            "description": "{plan}",
            "order_id": "{order_id}",

            "handler": function (response) {{
                window.location.href =
                    "?page=subscription&payment_id=" + response.razorpay_payment_id +
                    "&order_id={order_id}" +
                    "&signature=" + response.razorpay_signature;
            }},

            "theme": {{
                "color": "#00ff88"
            }}
        }};

        var rzp = new Razorpay(options);
        rzp.open();
    </script>

    </body>
    </html>
    """

    components.html(checkout_html, height=700, scrolling=False)
