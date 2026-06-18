import streamlit as st
from typing import Any, Dict, Optional
from datetime import datetime, timezone

from utils.db import get_supabase, require_user
from subscriptions.utils import plan_name
from auth import TEXT_MUTED, ACCENT


# -----------------------------
# SAFE HELPERS
# -----------------------------
def _safe_get_dict(data: Any) -> Dict[str, Any]:
    return data if isinstance(data, dict) else {}


def _safe_parse_iso(dt: Any) -> Optional[datetime]:
    """Parse ISO timestamps safely and normalize to UTC (naive)."""
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
# Subscription Fetcher (FINAL)
# -----------------------------
def get_user_active_subscription(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Returns the latest valid active subscription.
    Matches webhook logic:
    - status = active
    - expires_at must be in the future
    """
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

    # Validate expiry
    exp_dt = _safe_parse_iso(sub.get("expires_at"))
    if exp_dt is None:
        return None

    if exp_dt < datetime.utcnow():
        return None

    return sub


# -----------------------------
# UI Components
# -----------------------------
def render_subscription_card(sub: Optional[Dict[str, Any]]):
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

    plan_code = str(sub.get("plan_code", "FREE"))
    expires = str(sub.get("expires_at", "N/A"))

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


def render_quick_links():
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


def render_welcome_card(name: str):
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


# -----------------------------
# Main Dashboard Renderer (PATCHED)
# -----------------------------
def render_dashboard(sb=None, user=None):
    # Restore Supabase session
    if sb is None:
        sb = get_supabase()

    # Require authenticated user
    res = sb.auth.get_user()
    user = res.user if res else None

    if not user:
        st.error("You are not logged in.")
        st.stop()

    user_id = user.id
    name = user.user_metadata.get("full_name") or user.email or "Student"

    # Header
    st.markdown(
        """
        <h3 style="margin-top:0;">Your Dashboard</h3>
        <p style="color:#9ca3af; margin-top:-8px;">
            Quick overview of your learning and subscription status.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Layout
    col1, col2 = st.columns(2)

    with col1:
        sub = get_user_active_subscription(user_id)
        render_subscription_card(sub)

    with col2:
        render_quick_links()

    render_welcome_card(name)
