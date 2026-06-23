import streamlit as st
from typing import Any, Dict, Optional
from datetime import datetime, timezone

from utils.db import get_supabase, require_user
from subscriptions.utils import plan_name
from auth import TEXT_MUTED, ACCENT


# ---------------------------------------------------------
# SAFE HELPERS
# ---------------------------------------------------------
def _safe_get_dict(data: Any) -> Dict[str, Any]:
    return data if isinstance(data, dict) else {}


def _safe_parse_iso(dt: Any) -> Optional[datetime]:
    """Parse ISO timestamps safely and normalize to UTC."""
    if not isinstance(dt, str):
        return None
    try:
        parsed = datetime.fromisoformat(dt)
        if parsed.tzinfo:
            parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
        return parsed
    except Exception:
        return None


# ---------------------------------------------------------
# ACTIVE SUBSCRIPTION FETCHER
# ---------------------------------------------------------
def get_user_active_subscription(user_id: str) -> Optional[Dict[str, Any]]:
    sb = get_supabase()

    try:
        res = (
            sb.table("subscriptions")
            .select("*")
            .eq("user_id", user_id)
            .eq("status", "active")
            .order("expires_at", desc=True)
            .limit(1)
            .execute()
        )
    except Exception:
        return None

    rows = res.data or []
    if not rows:
        return None

    sub = _safe_get_dict(rows[0])

    exp_dt = _safe_parse_iso(sub.get("expires_at"))
    if exp_dt is None:
        return None

    if exp_dt < datetime.utcnow():
        return None

    return sub


# ---------------------------------------------------------
# SUBSCRIPTION CARD
# ---------------------------------------------------------
def render_subscription_card(sub: Optional[Dict[str, Any]]) -> None:
    if sub is None:
        st.markdown(
            f"""
            <div class="neon-card">
                <h4 style="margin:0;">No Active Plan</h4>
                <p style="color:{TEXT_MUTED}; margin:4px 0 0 0;">
                    Upgrade to unlock all chapters, notes, and quizzes.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    plan_code = str(sub.get("plan_code") or "FREE")
    expires = str(sub.get("expires_at") or "N/A")

    st.markdown(
        f"""
        <div class="neon-card">
            <h4 style="margin:0;">Active Plan</h4>
            <p style="color:{TEXT_MUTED}; margin:4px 0 0 0;">
                {plan_name(plan_code)}
            </p>
            <p style="margin:6px 0 0 0; color:{ACCENT}; font-weight:600;">
                Expires: {expires}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# QUICK LINKS CARD
# ---------------------------------------------------------
def render_quick_links() -> None:
    st.markdown(
        f"""
        <div class="neon-card">
            <h4 style="margin:0;">Quick Links</h4>
            <ul style="color:{TEXT_MUTED}; margin-top:6px;">
                <li>View Chapters</li>
                <li>Manage Subscription</li>
                <li>Billing History</li>
                <li>Math & News</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# WELCOME CARD
# ---------------------------------------------------------
def render_welcome_card(name: str) -> None:
    st.markdown(
        f"""
        <div class="neon-card" style="margin-top:16px;">
            <h4 style="margin:0;">Welcome, {name} 👋</h4>
            <p style="color:{TEXT_MUTED}; margin:4px 0 0 0;">
                Continue learning with structured chapters, notes, and practice.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# MAIN DASHBOARD RENDERER
# ---------------------------------------------------------
def render_dashboard(sb=None, user=None) -> None:
    user_dict: Dict[str, Any] = require_user()

    user_id = str(user_dict.get("id") or "")
    if not user_id:
        st.error("Invalid user session.")
        st.stop()

    name = (
        user_dict.get("full_name")
        or user_dict.get("email")
        or "Student"
    )

    if sb is None:
        sb = get_supabase()

    st.markdown(
        """
        <h3 style="margin-top:0;">Your Dashboard</h3>
        <p style="color:#9ca3af; margin-top:-8px;">
            Quick overview of your learning and subscription status.
        </p>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        sub = get_user_active_subscription(user_id)
        render_subscription_card(sub)

    with col2:
        render_quick_links()

    render_welcome_card(name)
