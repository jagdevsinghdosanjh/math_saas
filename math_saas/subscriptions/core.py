import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import razorpay
from math_saas.utils.db import get_supabase


RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")


def get_razorpay_client() -> Any:
    if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
        raise RuntimeError("Razorpay keys not configured in environment.")
    # Pylance: treat client as Any because SDK is dynamic
    return razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


def _plan_to_amount_and_duration(plan_code: str) -> Dict[str, Any]:
    # amounts in paise (INR * 100)
    if plan_code == "ANNUAL":
        return {"amount": 49900, "days": 365}  # ₹499.00
    if plan_code == "MONTHLY":
        return {"amount": 9900, "days": 30}    # ₹99.00
    raise ValueError(f"Unknown plan_code: {plan_code}")


def create_subscription_order(user_id: str, plan_code: str) -> Optional[Dict[str, Any]]:
    """
    1) Create Razorpay order
    2) Create pending subscription row
    3) Return order info (id, amount, etc.)
    """
    sb = get_supabase()
    client: Any = get_razorpay_client()

    plan_meta = _plan_to_amount_and_duration(plan_code)
    amount_paise: int = int(plan_meta["amount"])

    # 1. Create Razorpay order
    order: Any = client.order.create(
        {
            "amount": amount_paise,
            "currency": "INR",
            "payment_capture": 1,
        }
    )

    order_id: str = str(order.get("id"))

    # 2. Create pending subscription row
    sub_resp: Any = (
        sb.table("subscriptions")
        .insert(
            {
                "user_id": user_id,
                "plan": plan_code,
                "plan_code": plan_code,
                "status": "pending",
                "amount": amount_paise,
                "currency": "INR",
                "razorpay_order_id": order_id,
            }
        )
        .execute()
    )

    data = getattr(sub_resp, "data", None)
    sub_data: Optional[Dict[str, Any]] = None
    if isinstance(data, list) and data:
        sub_data = data[0]
    elif isinstance(data, dict):
        sub_data = data

    if not sub_data:
        return None

    return {
        "order_id": order_id,
        "amount": amount_paise,
        "currency": "INR",
        "subscription_id": sub_data.get("id"),
    }


def activate_subscription(
    user_id: str,
    razorpay_order_id: str,
    razorpay_payment_id: str,
    razorpay_signature: str,
) -> Dict[str, Any]:
    """
    Called from payment_callback after verifying signature.
    Updates subscriptions + subscription_payments + profiles.subscription_status.
    """
    sb = get_supabase()
    client: Any = get_razorpay_client()

    # 1. Fetch subscription row by order_id
    sub_resp: Any = (
        sb.table("subscriptions")
        .select("*")
        .eq("razorpay_order_id", razorpay_order_id)
        .single()
        .execute()
    )
    subscription: Any = getattr(sub_resp, "data", None)
    if not isinstance(subscription, dict):
        return {"success": False, "error": "Subscription not found for this order."}

    subscription_id: str = str(subscription.get("id"))
    plan_code: str = str(subscription.get("plan_code", "UNKNOWN"))

    # 2. Verify signature
    try:
        client.utility.verify_payment_signature(
            {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            }
        )
    except Exception as exc:
        # keep it simple; Pylance doesn’t know razorpay.errors
        return {"success": False, "error": f"Signature verification failed: {exc}"}

    # 3. Compute expiry
    plan_meta = _plan_to_amount_and_duration(plan_code)
    days: int = int(plan_meta["days"])
    now = datetime.utcnow()
    expires_at = now + timedelta(days=days)

    # 4. Update subscription row → active
    sb.table("subscriptions").update(
        {
            "status": "active",
            "started_at": now.isoformat() + "Z",
            "expires_at": expires_at.isoformat() + "Z",
        }
    ).eq("id", subscription_id).execute()

    # 5. Insert into subscription_payments
    sb.table("subscription_payments").insert(
        {
            "user_id": user_id,
            "order_id": razorpay_order_id,
            "payment_id": razorpay_payment_id,
            "signature": razorpay_signature,
            "amount": subscription.get("amount"),
            "status": "success",
            "subscription_id": subscription_id,
        }
    ).execute()

    # 6. Update profiles.subscription_status
    sb.table("profiles").update(
        {"subscription_status": "active"}
    ).eq("id", user_id).execute()

    return {"success": True}
