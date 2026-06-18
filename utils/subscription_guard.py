import streamlit as st
from datetime import datetime
from typing import Any, Dict, Optional

from utils.db import get_supabase


# -----------------------------
# SAFE HELPERS
# -----------------------------
def _safe_get_dict(data: Any) -> Dict[str, Any]:
    return data if isinstance(data, dict) else {}

from datetime import datetime, timezone

def _safe_parse_iso(dt: Any) -> Optional[datetime]:
    if not isinstance(dt, str):
        return None
    try:
        parsed = datetime.fromisoformat(dt)
        if parsed.tzinfo is not None:
            return parsed.astimezone(timezone.utc).replace(tzinfo=None)
        return parsed
    except Exception:
        return None

# -----------------------------
# FETCH ACTIVE SUBSCRIPTION
# -----------------------------
def _fetch_active_subscription(user_id: str) -> Optional[Dict[str, Any]]:
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

    rows = res.data or []
    if not rows:
        return None

    sub = _safe_get_dict(rows[0])

    exp_raw = sub.get("expires_at")
    exp_dt = _safe_parse_iso(exp_raw)

    if exp_dt is None:
        return None

    if exp_dt < datetime.utcnow():
        return None

    return sub


# -----------------------------
# MAIN ACCESS GUARD
# -----------------------------
def require_active_subscription():
    """
    Blocks access to premium pages unless:
    - user is logged in
    - user has an active, non-expired subscription
    """

    student = st.session_state.get("student")

    if not isinstance(student, dict):
        st.error("Please login to continue.")
        st.stop()

    user_id = str(student.get("id", ""))

    if not user_id:
        st.error("Invalid user session. Please login again.")
        st.stop()

    sub = _fetch_active_subscription(user_id)

    if sub is None:
        st.error("You do not have an active subscription.")
        st.info("Please purchase or renew your subscription to access this content.")
        st.stop()

    # Subscription is valid → allow access
    return sub
