from __future__ import annotations
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List

from math_saas.utils.db import get_supabase


# -----------------------------------------
# PLAN DURATIONS
# -----------------------------------------
PLAN_DURATIONS: Dict[str, int] = {
    "FREE": 3650,
    "MONTHLY": 30,
    "ANNUAL": 365,
}


# -----------------------------------------
# EXPIRY CALCULATOR
# -----------------------------------------
def _compute_expiry(plan_code: str) -> Dict[str, datetime]:
    now = datetime.utcnow()
    days = PLAN_DURATIONS.get(plan_code.upper(), 30)
    return {
        "started_at": now,
        "expires_at": now + timedelta(days=days),
    }


# -----------------------------------------
# CREATE SUBSCRIPTION
# -----------------------------------------
def create_subscription(
    user_id: str,
    plan_code: str,
    status: str,
    amount: Optional[int] = None,
    currency: Optional[str] = None,
    razorpay_order_id: Optional[str] = None,
) -> Dict[str, Any]:
    sb = get_supabase()
    times = _compute_expiry(plan_code)

    payload: Dict[str, Any] = {
        "user_id": user_id,
        "plan": plan_code.upper(),
        "plan_code": plan_code.upper(),
        "status": status,
        "amount": amount,
        "currency": currency,
        "razorpay_order_id": razorpay_order_id,
        "started_at": times["started_at"].isoformat(),
        "expires_at": times["expires_at"].isoformat(),
    }

    res = sb.table("subscriptions").insert(payload).execute()

    data: Optional[List[Dict[str, Any]]] = res.data  # type: ignore
    if data and isinstance(data, list) and len(data) > 0:
        return data[0]

    return {}


# -----------------------------------------
# ACTIVATE SUBSCRIPTION (AFTER PAYMENT)
# -----------------------------------------
def activate_subscription(order_id: str, payment_id: str, signature: str) -> None:
    sb = get_supabase()

    # Fetch subscription by order_id
    res = (
        sb.table("subscriptions")
        .select("*")
        .eq("razorpay_order_id", order_id)
        .single()
        .execute()
    )

    sub: Optional[Dict[str, Any]] = res.data  # type: ignore
    if not sub or not isinstance(sub, dict):
        return

    plan_code = str(sub.get("plan_code", "FREE"))
    times = _compute_expiry(plan_code)

    # Update subscription
    sb.table("subscriptions").update(
        {
            "status": "active",
            "started_at": times["started_at"].isoformat(),
            "expires_at": times["expires_at"].isoformat(),
        }
    ).eq("id", sub["id"]).execute()

    # Log payment
    sb.table("subscription_payments").insert(
        {
            "user_id": sub.get("user_id"),
            "order_id": order_id,
            "payment_id": payment_id,
            "signature": signature,
            "amount": sub.get("amount"),
            "status": "success",
        }
    ).execute()


# -----------------------------------------
# GET LATEST SUBSCRIPTION
# -----------------------------------------
def get_latest_subscription(user_id: str) -> Optional[Dict[str, Any]]:
    sb = get_supabase()

    res = (
        sb.table("subscriptions")
        .select("*")
        .eq("user_id", user_id)
        .order("started_at", desc=True)
        .limit(1)
        .execute()
    )

    data: Optional[List[Dict[str, Any]]] = res.data  # type: ignore

    if data and isinstance(data, list) and len(data) > 0:
        return data[0]

    return None

def get_active_subscription(user_id: str) -> Optional[Dict[str, Any]]:
    sb = get_supabase()

    res = (
        sb.table("subscriptions")
        .select("*")
        .eq("user_id", user_id)
        .eq("status", "active")
        .order("expires_at", desc=True)
        .limit(1)
        .execute()
    )

    data = res.data or []
    if not data:
        return None

    item = data[0]

    # Ensure return type is Dict[str, Any]
    if isinstance(item, dict):
        return item

    return None
