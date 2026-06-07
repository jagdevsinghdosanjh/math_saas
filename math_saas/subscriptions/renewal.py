import datetime as dt
from typing import Any, Dict, List, Optional #noqa

from math_saas.utils.db import get_supabase
from math_saas.subscriptions.plans import PLANS


# -----------------------------
# Check if subscription is expired
# -----------------------------
def is_expired(sub: Dict[str, Any]) -> bool:
    expires_raw = sub.get("expires_at")
    if not isinstance(expires_raw, str):
        return True

    expires_at = dt.datetime.fromisoformat(expires_raw)
    return expires_at < dt.datetime.utcnow()


# -----------------------------
# Auto-expire all outdated subscriptions
# -----------------------------
def expire_old_subscriptions():
    sb = get_supabase()
    now_iso = dt.datetime.utcnow().isoformat()

    sb.table("subscriptions").update(
        {"status": "expired"}
    ).lt("expires_at", now_iso).eq("status", "active").execute()


# -----------------------------
# Manual renewal (admin or user)
# -----------------------------
def renew_subscription(user_id: str, plan_code: str) -> Optional[Dict[str, Any]]:
    sb = get_supabase()

    now = dt.datetime.utcnow()
    duration = PLANS[plan_code]["duration_days"]
    new_expiry = now + dt.timedelta(days=duration)

    res = (
        sb.table("subscriptions")
        .insert(
            {
                "user_id": user_id,
                "plan_code": plan_code,
                "status": "active",
                "amount": PLANS[plan_code]["price_inr"] * 100,
                "currency": "INR",
                "started_at": now.isoformat(),
                "expires_at": new_expiry.isoformat(),
            }
        )
        .execute()
    )

    raw = res.data or []
    return raw[0] if raw and isinstance(raw[0], dict) else None


# -----------------------------
# Days remaining in subscription
# -----------------------------
def days_remaining(sub: Dict[str, Any]) -> int:
    expires_raw = sub.get("expires_at")
    if not isinstance(expires_raw, str):
        return 0

    expires_at = dt.datetime.fromisoformat(expires_raw)
    delta = expires_at - dt.datetime.utcnow()
    return max(delta.days, 0)

# import datetime as dt
# from typing import Any, Dict, List, Optional #noqa

# from math_saas.utils.db import get_supabase
# from math_saas.subscriptions.plans import PLANS
# from math_saas.subscriptions.core import get_active_subscription #noqa


# # -----------------------------
# # Check if subscription is expired
# # -----------------------------
# def is_expired(sub: Dict[str, Any]) -> bool:
#     expires_raw = sub.get("expires_at")
#     if not isinstance(expires_raw, str):
#         return True

#     expires_at = dt.datetime.fromisoformat(expires_raw)
#     return expires_at < dt.datetime.utcnow()


# # -----------------------------
# # Renew subscription manually
# # -----------------------------
# def renew_subscription(user_id: str, plan_code: str) -> Optional[Dict[str, Any]]:
#     sb = get_supabase()

#     now = dt.datetime.utcnow()
#     duration = PLANS[plan_code]["duration_days"]
#     new_expiry = now + dt.timedelta(days=duration)

#     res = (
#         sb.table("subscriptions")
#         .insert(
#             {
#                 "user_id": user_id,
#                 "plan_code": plan_code,
#                 "status": "active",
#                 "amount": PLANS[plan_code]["price_inr"] * 100,
#                 "currency": "INR",
#                 "started_at": now.isoformat(),
#                 "expires_at": new_expiry.isoformat(),
#             }
#         )
#         .execute()
#     )

#     raw = res.data or []
#     return raw[0] if raw and isinstance(raw[0], dict) else None


# # -----------------------------
# # Auto-expire subscriptions
# # -----------------------------
# def expire_old_subscriptions():
#     sb = get_supabase()

#     now_iso = dt.datetime.utcnow().isoformat()

#     sb.table("subscriptions").update(
#         {"status": "expired"}
#     ).lt("expires_at", now_iso).eq("status", "active").execute()


# # -----------------------------
# # Get days remaining
# # -----------------------------
# def days_remaining(sub: Dict[str, Any]) -> int:
#     expires_raw = sub.get("expires_at")
#     if not isinstance(expires_raw, str):
#         return 0

#     expires_at = dt.datetime.fromisoformat(expires_raw)
#     delta = expires_at - dt.datetime.utcnow()
#     return max(delta.days, 0)
