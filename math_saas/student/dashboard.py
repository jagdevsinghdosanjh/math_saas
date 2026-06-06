import streamlit as st
from math_saas.subscriptions.core import get_active_subscription
from math_saas.subscriptions.utils import format_inr, plan_name #noqa
from math_saas.auth import TEXT_MUTED, TEXT_MAIN, ACCENT #noqa


def render_dashboard():
    student = st.session_state.get("student")
    if not student:
        st.error("Please login as student.")
        return

    user_id = student["id"]

    # Fetch subscription
    sub = get_active_subscription(user_id)

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

    # -----------------------------
    # CARD 1 — Active Subscription
    # -----------------------------
    with col1:
        if sub:
            st.markdown(
                f"""
                <div class="neon-card">
                    <h4 style="margin:0;">Active Plan</h4>
                    <p style="color:{TEXT_MUTED}; margin:4px 0 0 0;">
                        {plan_name(sub.get("plan_code", ""))}
                    </p>
                    <p style="margin:6px 0 0 0; color:{ACCENT}; font-weight:600;">
                        Expires: {sub.get("expires_at", "")}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
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

    # -----------------------------
    # CARD 2 — Quick Links
    # -----------------------------
    with col2:
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

    # -----------------------------
    # CARD 3 — Welcome Message
    # -----------------------------
    st.markdown(
        f"""
        <div class="neon-card" style="margin-top:16px;">
            <h4 style="margin:0;">Welcome, {student.get("name", "Student")} 👋</h4>
            <p style="color:{TEXT_MUTED}; margin:4px 0 0 0;">
                Continue learning with structured chapters, notes, and practice.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
