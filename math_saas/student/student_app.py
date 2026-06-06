import streamlit as st

from math_saas.auth import (
    require_student,
    logout,
    app_container_style,
    top_bar,
)

from math_saas.student.subscriptions_page import render_subscriptions_page
from math_saas.student.billing_history import render_billing_history
from math_saas.student.dashboard import render_dashboard
from math_saas.student.chapters_page import render_chapters_page


def run_student():
    app_container_style()

    # handle logout via query param
    if st.query_params.get("student_logout") == "true":
        logout()

    require_student()
    top_bar("Math Hub Student Portal", "Student", "student_logout")

    st.markdown(
        """
        <div class="neon-card" style="margin-top:16px; margin-bottom:10px;">
            <h4 style="margin:0 0 4px 0;">Welcome back 👋</h4>
            <p style="margin:0; color:#9ca3af; font-size:0.9rem;">
                Continue your learning journey with structured chapters, notes, and practice.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_dashboard, tab_chapters, tab_subs, tab_billing = st.tabs(
        ["Dashboard", "Chapters", "Subscription", "Billing"]
    )

    with tab_dashboard:
        try:
            render_dashboard()
        except Exception:
            st.info("Dashboard coming soon.")

    with tab_chapters:
        try:
            render_chapters_page()
        except Exception:
            st.info("Chapters page coming soon.")

    with tab_subs:
        render_subscriptions_page()

    with tab_billing:
        render_billing_history()
