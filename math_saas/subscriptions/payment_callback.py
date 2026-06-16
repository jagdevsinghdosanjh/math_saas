from typing import Dict, Any

from math_saas.utils.db import get_supabase
from math_saas.subscriptions.core import activate_subscription


def handle_payment_callback(
    order_id: str,
    payment_id: str,
    signature: str,
) -> Dict[str, Any]:
    """
    Called when Razorpay redirects back with order_id, payment_id, signature in query params.
    """
    sb = get_supabase()

    sub_resp: Any = (
        sb.table("subscriptions")
        .select("user_id")
        .eq("razorpay_order_id", order_id)
        .single()
        .execute()
    )
    sub: Any = getattr(sub_resp, "data", None)
    if not isinstance(sub, dict):
        return {"success": False, "error": "Subscription not found for this order."}

    user_id: str = str(sub.get("user_id"))

    result = activate_subscription(
        user_id=user_id,
        razorpay_order_id=order_id,
        razorpay_payment_id=payment_id,
        razorpay_signature=signature,
    )

    if not result.get("success"):
        return {"success": False, "error": str(result.get("error", "Unknown error"))}

    return {"success": True, "error": ""}
