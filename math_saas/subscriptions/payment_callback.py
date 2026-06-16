from typing import Dict, Any
from math_saas.utils.db import get_supabase
from math_saas.subscriptions.core import activate_subscription
import streamlit as st


def handle_payment_callback(order_id: str, payment_id: str, signature: str) -> Dict[str, Any]:
    """
    DEBUG VERSION — prints everything to Streamlit so we can see
    why activation is failing.
    """

    st.warning("🔍 DEBUG: Razorpay callback triggered")

    st.write("### 🔧 Raw callback parameters received:")
    st.json({
        "order_id": order_id,
        "payment_id": payment_id,
        "signature": signature
    })

    # 1. Fetch subscription row
    sb = get_supabase()
    sub_resp = (
        sb.table("subscriptions")
        .select("*")
        .eq("razorpay_order_id", order_id)
        .single()
        .execute()
    )

    subscription = getattr(sub_resp, "data", None)

    st.write("### 📦 Subscription row fetched from Supabase:")
    st.json(subscription)

    if not isinstance(subscription, dict):
        return {
            "success": False,
            "error": "Subscription not found for this order_id (DEBUG: order_id mismatch)"
        }

    user_id = subscription.get("user_id")

    st.write("### 👤 User ID from subscription row:")
    st.write(user_id)

    # 2. Try activation
    st.write("### 🚀 Attempting activation…")

    result = activate_subscription(
        user_id=str(user_id),
        razorpay_order_id=order_id,
        razorpay_payment_id=payment_id,
        razorpay_signature=signature,
    )

    st.write("### 🧪 Activation result:")
    st.json(result)

    if not result.get("success"):
        return {
            "success": False,
            "error": f"Activation failed (DEBUG): {result.get('error')}"
        }

    st.success("🎉 DEBUG: Activation succeeded!")
    return {"success": True}
