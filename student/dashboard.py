import streamlit as st
from typing import Any, Dict, Optional
from datetime import datetime

from utils.db import get_supabase
from subscriptions.utils import plan_name
from auth import TEXT_MUTED, ACCENT


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

# def _safe_parse_iso(dt: Any) -> Optional[datetime]:
#     if isinstance(dt, str):
#         try:
#             return datetime.fromisoformat(dt)
#         except Exception:
#             return None
#     return None


# -----------------------------
# Subscription Fetcher (Corrected)
# -----------------------------
def get_user_active_subscription(user_id: str) -> Optional[Dict[str, Any]]:
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


def render_welcome_card(student: Dict[str, Any]):
    name = str(student.get("full_name") or student.get("name") or "Student")

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
# Main Dashboard Renderer
# -----------------------------
def render_dashboard():
    student = st.session_state.get("student")

    if not isinstance(student, dict):
        st.error("Please login as student.")
        return

    user_id = str(student.get("id", ""))

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

    render_welcome_card(student)
