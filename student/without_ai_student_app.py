import streamlit as st
from typing import Any, Dict

from auth import (
    require_student,
    logout,
    app_container_style,
    top_bar,
)
from utils.db import get_supabase, require_user

from student.dashboard import render_dashboard
from student.chapters_page import render_chapters_page
from student.subscriptions_page import render_subscriptions_page
from student.billing_history import render_billing_history
from student.public_content import render_public_content


# ---------------------------------------------------------
# QUIZ CHAPTERS
# ---------------------------------------------------------
def render_quiz_chapters() -> None:
    user: Dict[str, Any] = require_user()
    sb = get_supabase()

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
# MAIN STUDENT APP
# ---------------------------------------------------------
def run_student() -> None:
    app_container_style()

    user: Dict[str, Any] = require_user()
    require_student()

    sb = get_supabase()

    # ---------------------------------------------------------
    # LOGOUT
    # ---------------------------------------------------------
    params = st.query_params
    if params.get("student_logout") == "true":
        logout()
        return

    # ---------------------------------------------------------
    # NORMAL STUDENT UI
    # ---------------------------------------------------------
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

    tab_labels = [
        "Dashboard",
        "Chapters",
        "Quizzes",
        "Subscription",
        "Billing",
        "Math & News",
    ]

    (
        tab_dashboard,
        tab_chapters,
        tab_quiz,
        tab_subs,
        tab_billing,
        tab_public,
    ) = st.tabs(tab_labels)

    with tab_dashboard:
        render_dashboard()

    with tab_chapters:
        render_chapters_page()

    with tab_quiz:
        render_quiz_chapters()

    with tab_subs:
        render_subscriptions_page()

    with tab_billing:
        render_billing_history()

    with tab_public:
        render_public_content()
