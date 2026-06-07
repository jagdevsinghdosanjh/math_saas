import datetime as dt
from typing import Any, Dict, List, Optional

from utils.db import get_supabase
from subscriptions.plans import PLANS


# -----------------------------
# Normalize DB rows
# -----------------------------
def _clean_rows(raw: Any) -> List[Dict[str, Any]]:
    if not isinstance(raw, list):
        return []
    return [item for item in raw if isinstance(item, dict)]


# -----------------------------
# Fetch latest subscription (any status)
# -----------------------------
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

    data = _clean_rows(res.data)
    return data[0] if data else None


# -----------------------------
# Fetch active subscription
# -----------------------------
def get_active_subscription(user_id: str) -> Optional[Dict[str, Any]]:
    sb = get_supabase()

    now_iso = dt.datetime.utcnow().isoformat()

    res = (
        sb.table("subscriptions")
        .select("*")
        .eq("user_id", user_id)
        .eq("status", "active")
        .gte("ends_at", now_iso)          # FIXED: correct column
        .order("ends_at", desc=True)      # FIXED: correct column
        .limit(1)
        .execute()
    )

    data = _clean_rows(res.data)
    return data[0] if data else None


# -----------------------------
# Create a new subscription (free or paid)
# -----------------------------
def create_subscription(
    user_id: str,
    plan_code: str,
    status: str,
    amount: int,
    currency: str = "INR",
    razorpay_order_id: Optional[str] = None,
) -> Dict[str, Any]:

    sb = get_supabase()

    now = dt.datetime.utcnow()
    ends_at = now + dt.timedelta(days=PLANS[plan_code]["duration_days"])

    payload = {
        "user_id": user_id,
        "plan": plan_code,               # FIXED: your DB column is "plan"
        "status": status,
        "amount": amount,
        "currency": currency,
        "started_at": now.isoformat(),
        "ends_at": ends_at.isoformat(),  # FIXED: correct column
    }

    if razorpay_order_id:
        payload["razorpay_order_id"] = razorpay_order_id

    res = sb.table("subscriptions").insert(payload).execute()

    data = _clean_rows(res.data)
    return data[0] if data else payload


# -----------------------------
# Mark subscription as active after payment
# -----------------------------
def activate_subscription(order_id: str, payment_id: str, signature: str):
    sb = get_supabase()

    sb.table("subscriptions").update(
        {
            "status": "active",
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature,
        }
    ).eq("razorpay_order_id", order_id).execute()


# -----------------------------
# Expire a subscription manually
# -----------------------------
def expire_subscription(subscription_id: str):
    sb = get_supabase()

    sb.table("subscriptions").update(
        {"status": "expired"}
    ).eq("id", subscription_id).execute()


# -----------------------------
# Extend subscription duration
# -----------------------------
def extend_subscription(subscription_id: str, extra_days: int):
    sb = get_supabase()

    res = (
        sb.table("subscriptions")
        .select("*")
        .eq("id", subscription_id)
        .limit(1)
        .execute()
    )

    data = _clean_rows(res.data)
    if not data:
        return

    sub = data[0]
    ends_raw = sub.get("ends_at")

    if not isinstance(ends_raw, str):
        return

    old_ends = dt.datetime.fromisoformat(ends_raw)
    new_ends = old_ends + dt.timedelta(days=extra_days)

    sb.table("subscriptions").update(
        {"ends_at": new_ends.isoformat()}
    ).eq("id", subscription_id).execute()

# import datetime as dt
# from typing import Any, Dict, List, Optional

# from math_saas.utils.db import get_supabase
# from math_saas.subscriptions.plans import PLANS


# # -----------------------------
# # Fetch latest subscription (any status)
# # -----------------------------
# def get_latest_subscription(user_id: str) -> Optional[Dict[str, Any]]:
#     sb = get_supabase()

#     res = (
#         sb.table("subscriptions")
#         .select("*")
#         .eq("user_id", user_id)
#         .order("started_at", desc=True)
#         .limit(1)
#         .execute()
#     )

#     raw = res.data or []

#     data: List[Dict[str, Any]] = [
#         item for item in raw if isinstance(item, dict)
#     ]

#     return data[0] if data else None


# # -----------------------------
# # Fetch active subscription
# # -----------------------------
# def get_active_subscription(user_id: str) -> Optional[Dict[str, Any]]:
#     sb = get_supabase()

#     now_iso = dt.datetime.utcnow().isoformat()

#     res = (
#         sb.table("subscriptions")
#         .select("*")
#         .eq("user_id", user_id)
#         .eq("status", "active")
#         .gte("expires_at", now_iso)
#         .order("expires_at", desc=True)
#         .limit(1)
#         .execute()
#     )

#     raw = res.data or []

#     data: List[Dict[str, Any]] = [
#         item for item in raw if isinstance(item, dict)
#     ]

#     return data[0] if data else None


# # -----------------------------
# # Create a new subscription (free or paid)
# # -----------------------------
# def create_subscription(
#     user_id: str,
#     plan_code: str,
#     status: str,
#     amount: int,
#     currency: str = "INR",
#     razorpay_order_id: Optional[str] = None,
# ) -> Dict[str, Any]:

#     sb = get_supabase()

#     now = dt.datetime.utcnow()
#     expires = now + dt.timedelta(days=PLANS[plan_code]["duration_days"])

#     payload = {
#         "user_id": user_id,
#         "plan_code": plan_code,
#         "status": status,
#         "amount": amount,
#         "currency": currency,
#         "started_at": now.isoformat(),
#         "expires_at": expires.isoformat(),
#     }

#     if razorpay_order_id:
#         payload["razorpay_order_id"] = razorpay_order_id

#     res = sb.table("subscriptions").insert(payload).execute()

#     raw = res.data or []
#     data: List[Dict[str, Any]] = [
#         item for item in raw if isinstance(item, dict)
#     ]

#     return data[0] if data else payload


# # -----------------------------
# # Mark subscription as active after payment
# # -----------------------------
# def activate_subscription(order_id: str, payment_id: str, signature: str):
#     sb = get_supabase()

#     sb.table("subscriptions").update(
#         {
#             "status": "active",
#             "razorpay_payment_id": payment_id,
#             "razorpay_signature": signature,
#         }
#     ).eq("razorpay_order_id", order_id).execute()


# # -----------------------------
# # Expire a subscription manually
# # -----------------------------
# def expire_subscription(subscription_id: int):
#     sb = get_supabase()

#     sb.table("subscriptions").update(
#         {"status": "expired"}
#     ).eq("id", subscription_id).execute()


# # -----------------------------
# # Extend subscription duration
# # -----------------------------
# def extend_subscription(subscription_id: int, extra_days: int):
#     sb = get_supabase()

#     res = (
#         sb.table("subscriptions")
#         .select("*")
#         .eq("id", subscription_id)
#         .limit(1)
#         .execute()
#     )

#     raw = res.data or []
#     if not raw or not isinstance(raw[0], dict):
#         return

#     sub = raw[0]

#     expires_raw = sub.get("expires_at")

#     # Pylance-safe: ensure it's a string
#     if not isinstance(expires_raw, str):
#         return

#     old_expiry = dt.datetime.fromisoformat(expires_raw)
#     new_expiry = old_expiry + dt.timedelta(days=extra_days)

#     sb.table("subscriptions").update(
#         {"expires_at": new_expiry.isoformat()}
#     ).eq("id", subscription_id).execute()
