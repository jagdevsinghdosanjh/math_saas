import streamlit as st

from math_saas.auth import (
    require_student,
    logout,
    app_container_style,
    top_bar,
)
from math_saas.utils.db import get_supabase

from math_saas.student.dashboard import render_dashboard
from math_saas.student.chapters_page import render_chapters_page
from math_saas.student.subscriptions_page import render_subscriptions_page
from math_saas.student.billing_history import render_billing_history
from math_saas.student.public_content import render_public_content


# ---------------------------------------------------------
# QUIZ CHAPTERS (STATIC QUIZ SYSTEM)
# ---------------------------------------------------------
def render_quiz_chapters() -> None:
    sb = get_supabase()
    if sb is None:
        st.warning("Unable to connect to Supabase.")
        return

    try:
        res = (
            sb.table("chapters")
            .select("id, grade, board, chapter_key, chapter_name")
            .order("grade", desc=False)
            .execute()
        )
        chapters = res.data or []
    except Exception as exc:
        st.error(f"Error fetching chapters: {exc}")
        return

    if not chapters:
        st.info("No chapters available yet.")
        return

    st.subheader("📘 Chapters & Practice Quizzes")

    for ch in chapters:
        if not isinstance(ch, dict):
            continue

        title = ch.get("chapter_name", "Untitled")
        chapter_key = ch.get("chapter_key", "")

        quiz_url = (
            "https://jsdasr-math-cbse.vercel.app/9th-Math/index.html?"
            f"chapter={chapter_key}"
        )

        with st.expander(str(title or "Untitled")):
            st.write(f"Practice quizzes for **{title}**")
            st.markdown(
                f'<a href="{quiz_url}" target="_blank"><button>Start Quiz</button></a>',
                unsafe_allow_html=True,
            )


# ---------------------------------------------------------
# STUDENT PORTAL MAIN FUNCTION
# ---------------------------------------------------------
def run_student() -> None:
    app_container_style()

    # Logout via query params
    params = st.query_params
    if params.get("student_logout") == "true":
        logout()
        return
    require_student()

    top_bar("Math Hub Student Portal", "Student", "student_logout")

    # Welcome card
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

    tab_labels = [
        "Dashboard",
        "Chapters",
        "Quizzes",
        "Subscription",
        "Billing",
        "Math & News",
    ]

    tab_dashboard, tab_chapters, tab_quiz, tab_subs, tab_billing, tab_public = st.tabs(
        tab_labels
    )

    routes = {
        "Dashboard": render_dashboard,
        "Chapters": render_chapters_page,
        "Subscription": render_subscriptions_page,
        "Billing": render_billing_history,
        "Math & News": render_public_content,
    }

    with tab_dashboard:
        try:
            routes["Dashboard"]()
        except Exception as exc:
            st.info(f"Dashboard coming soon. ({exc})")

    with tab_chapters:
        try:
            routes["Chapters"]()
        except Exception as exc:
            st.info(f"Chapters page coming soon. ({exc})")

    with tab_quiz:
        try:
            render_quiz_chapters()
        except Exception as exc:
            st.info(f"Quizzes not available. ({exc})")

    with tab_subs:
        try:
            routes["Subscription"]()
        except Exception as exc:
            st.info(f"Subscription page coming soon. ({exc})")

    with tab_billing:
        try:
            routes["Billing"]()
        except Exception as exc:
            st.info(f"Billing page coming soon. ({exc})")

    with tab_public:
        try:
            routes["Math & News"]()
        except Exception as exc:
            st.info(f"Math & News page coming soon. ({exc})")