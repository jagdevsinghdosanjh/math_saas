import streamlit as st
from typing import Any, Dict
import streamlit.components.v1 as components

from utils.db import get_supabase
from utils.razorpay import get_razorpay_client, get_razorpay_keys
from subscriptions.utils import format_inr, plan_name


def render_razorpay_checkout() -> None:
    st.header("Razorpay Checkout")

    # ---------------------------------------------------------
    # Restore Supabase session + require authenticated user
    # ---------------------------------------------------------
    sb = get_supabase()
    res = sb.auth.get_user()
    user = res.user if res and res.user else None

    if not user:
        st.error("You are not logged in.")
        st.stop()

    # ---------------------------------------------------------
    # Razorpay client
    # ---------------------------------------------------------
    client = get_razorpay_client()
    if client is None:
        st.error("Razorpay keys not configured. Cannot start checkout.")
        return

    # ---------------------------------------------------------
    # Read query params
    # ---------------------------------------------------------
    params = st.query_params
    sub_id = params.get("sub_id", [""])[0]

    if not sub_id:
        st.error("Missing subscription ID.")
        return

    # ---------------------------------------------------------
    # Fetch subscription
    # ---------------------------------------------------------
    res = (
        sb.table("subscriptions")
        .select("id, user_id, amount, currency, plan, plan_code, status")
        .eq("id", sub_id)
        .single()
        .execute()
    )

    sub = res.data or {}
    if not isinstance(sub, Dict):
        st.error("Subscription not found.")
        return

    # ---------------------------------------------------------
    # Authorization check
    # ---------------------------------------------------------
    if str(sub.get("user_id")) != user.id:
        st.error("Unauthorized access to subscription.")
        st.stop()

    # ---------------------------------------------------------
    # Extract subscription details (Pylance-safe)
    # ---------------------------------------------------------
    raw_amount = sub.get("amount")

    if isinstance(raw_amount, (int, float)):
        amount = int(raw_amount)
    elif isinstance(raw_amount, str) and raw_amount.isdigit():
        amount = int(raw_amount)
    else:
        amount = 0

    currency = str(sub.get("currency") or "INR")
    plan_code = str(sub.get("plan_code") or "")
    plan = plan_name(plan_code)

    # ---------------------------------------------------------
    # Create Razorpay order
    # ---------------------------------------------------------
    try:
        order = client.order.create({  # type: ignore[attr-defined]
            "amount": amount,
            "currency": currency,
            "payment_capture": 1,
            "notes": {
                "subscription_id": str(sub_id),
                "user_id": user.id,
                "plan_code": plan_code,
            },
        })
    except Exception as exc:
        st.error(f"Failed to create Razorpay order. ({exc})")
        return

    order_id = str(order.get("id"))

    # ---------------------------------------------------------
    # Save order_id in subscriptions
    # ---------------------------------------------------------
    sb.table("subscriptions").update({
        "razorpay_order_id": order_id,
    }).eq("id", sub_id).execute()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------
    st.markdown("### Complete Payment")
    st.write(f"Plan: **{plan}**")
    st.write(f"Amount: **{format_inr(amount)}**")

    key_id, _ = get_razorpay_keys()

    # ---------------------------------------------------------
    # Razorpay Checkout.js Embed (auto-open only once)
    # ---------------------------------------------------------
    checkout_html = f"""
    <script src="https://checkout.razorpay.com/v1/checkout.js"></script>

    <script>
        if (!window.rzp_opened) {{
            window.rzp_opened = true;

            var options = {{
                "key": "{key_id}",
                "amount": "{amount}",
                "currency": "{currency}",
                "name": "Math Hub",
                "description": "{plan}",
                "order_id": "{order_id}",

                "handler": function (response) {{
                    window.location.href =
                        "?page=subscriptions&payment_id=" + response.razorpay_payment_id +
                        "&order_id={order_id}" +
                        "&signature=" + response.razorpay_signature;
                }},

                "theme": {{
                    "color": "#00ff88"
                }}
            }};

            var rzp = new Razorpay(options);
            rzp.open();
        }}
    </script>
    """

    components.html(checkout_html, height=700, scrolling=False)
