import streamlit as st
from typing import Any, Dict, Optional

from supabase import create_client
from math_saas.config import SUPABASE_URL, SUPABASE_KEY
from math_saas.subscriptions.utils import plan_name
from math_saas.auth import TEXT_MUTED, ACCENT


# -----------------------------
# Supabase Client (Type Safe)
# -----------------------------
assert SUPABASE_URL is not None, "SUPABASE_URL missing"
assert SUPABASE_KEY is not None, "SUPABASE_KEY missing"

sb = create_client(SUPABASE_URL, SUPABASE_KEY)


# -----------------------------
# Subscription Fetcher
# -----------------------------
def get_user_active_subscription(user_id: str) -> Optional[Dict[str, Any]]:
    """Return active subscription row as a dictionary."""
    res = (
        sb.table("subscriptions")
        .select("*")
        .eq("user_id", user_id)
        .eq("status", "active")
        .single()
        .execute()
    )
    data = res.data
    return data if isinstance(data, dict) else None


# -----------------------------
# UI Components
# -----------------------------
def render_subscription_card(sub: Optional[Dict[str, Any]]):
    """Render the subscription card safely."""
    if sub is None:
        st.markdown(
            f"""
            <div class="neon-card">
                <h4 style="margin:0;">No Active Plan</h4>
                <p style="color:{TEXT_MUTED}; margin:4px 0 0 0;">
                    Upgrade to unlock all chapters and notes.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Safe extraction
    plan_code = str(sub.get("plan_code", ""))
    expires = str(sub.get("expires_at", ""))

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
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_welcome_card(student: Dict[str, Any]):
    name = str(student.get("name", "Student"))
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

    # Subscription Card
    with col1:
        sub = get_user_active_subscription(user_id)
        render_subscription_card(sub)

    # Quick Links
    with col2:
        render_quick_links()

    # Welcome Card
    render_welcome_card(student)
