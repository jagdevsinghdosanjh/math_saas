import streamlit as st
from typing import Dict, List, Any

from auth import (
    require_student,
    logout,
    app_container_style,
    top_bar,
)

from utils.db import get_supabase, require_user

# Student pages
from student.dashboard import render_dashboard
from student.chapters_page import render_chapters_page
from student.subscriptions_page import render_subscriptions_page
from student.billing_history import render_billing_history
from student.public_content import render_public_content

# AI services
from services.solver import solve_stepwise
from services.question_generator import generate_questions
from services.summary import summarize_chapter


# ---------------------------------------------------------
# QUIZ CHAPTERS (Refactored)
# ---------------------------------------------------------
def render_quiz_chapters() -> None:
    user = require_user()

    # Handle dict vs Pydantic user
    if isinstance(user, dict):
        meta = user
    else:
        meta = getattr(user, "user_metadata", {}) or {}

    student_name = (
        meta.get("full_name")
        or meta.get("name")
        or meta.get("email", "")
    ).replace(" ", "%20")

    sb = get_supabase()

    try:
        res = (
            sb.table("sync_chapters")
            .select("id, grade, chapter_title")
            .order("grade", desc=False)
            .order("id", desc=False)
            .execute()
        )
        raw_data = res.data
    except Exception as exc:
        st.error(f"Error fetching quiz chapters: {exc}")
        return

    if not isinstance(raw_data, list):
        st.info("No quiz chapters available yet.")
        return

    chapters = [ch for ch in raw_data if isinstance(ch, dict)]

    if not chapters:
        st.info("No quiz chapters available yet.")
        return

    st.subheader("📘 Class‑wise Practice Quizzes")

    grouped: Dict[str, List[Dict[str, Any]]] = {"9": [], "10": []}

    for ch in chapters:
        grade = str(ch.get("grade", "")).strip()
        if grade in grouped:
            grouped[grade].append(ch)

    # -------------------------
    # CLASS 9
    # -------------------------
    if grouped["9"]:
        st.markdown("## 🟦 Class 9")
        for ch in grouped["9"]:
            title = str(ch.get("chapter_title", "Untitled"))
            safe_title = title.replace(" ", "%20")

            quiz_url = (
                f"https://jsdasr-math-cbse.vercel.app/9th-Math/index.html?"
                f"chapter={safe_title}&name={student_name}"
            )

            with st.expander(title):
                st.write(f"Practice quizzes for **{title}**")
                st.markdown(
                    f'<a href="{quiz_url}" target="_blank"><button>Start Quiz</button></a>',
                    unsafe_allow_html=True,
                )

    # -------------------------
    # CLASS 10
    # -------------------------
    if grouped["10"]:
        st.markdown("## 🟥 Class 10")
        for ch in grouped["10"]:
            title = str(ch.get("chapter_title", "Untitled"))
            safe_title = title.replace(" ", "%20")

            quiz_url = (
                f"https://jsdasr-math-cbse.vercel.app/10th-Math/index.html?"
                f"chapter={safe_title}&name={student_name}"
            )

            with st.expander(title):
                st.write(f"Practice quizzes for **{title}**")
                st.markdown(
                    f'<a href="{quiz_url}" target="_blank"><button>Start Quiz</button></a>',
                    unsafe_allow_html=True,
                )


# ---------------------------------------------------------
# MAIN STUDENT APP (Refactored)
# ---------------------------------------------------------
def run_student() -> None:
    app_container_style()

    # Restore user & role
    require_user()
    require_student()

    # Logout via query params
    params = st.query_params
    if params.get("student_logout") == "true":
        logout()
        return

    # Top bar
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

    # Tabs
    tab_labels = [
        "Dashboard",
        "Chapters",
        "Quizzes",
        "Subscription",
        "Billing",
        "Math & News",
        "AI Tutor",
        "Worksheet Generator",
        "Chapter Notes",
    ]

    (
        tab_dashboard,
        tab_chapters,
        tab_quiz,
        tab_subs,
        tab_billing,
        tab_public,
        tab_ai_tutor,
        tab_worksheet,
        tab_notes,
    ) = st.tabs(tab_labels)

    # Dashboard
    with tab_dashboard:
        render_dashboard()

    # Chapters
    with tab_chapters:
        render_chapters_page()

    # Quizzes
    with tab_quiz:
        render_quiz_chapters()

    # Subscription
    with tab_subs:
        render_subscriptions_page()

    # Billing
    with tab_billing:
        render_billing_history()

    # Public content
    with tab_public:
        render_public_content()

    # AI Tutor
    with tab_ai_tutor:
        st.subheader("🤖 AI Tutor – Explain My Mistake")

        student_answer = st.text_area("Paste your incorrect solution")

        if st.button("Explain My Mistake"):
            if student_answer.strip():
                with st.spinner("Analyzing your solution..."):
                    result = solve_stepwise(student_answer)

                st.subheader("Explanation")
                for i, step in enumerate(result.get("steps", []), start=1):
                    st.markdown(f"**Step {i}:** {step}")

                st.subheader("Final Answer")
                st.write(result.get("final_answer", ""))
            else:
                st.warning("Please paste your solution first.")

    # Worksheet Generator
    with tab_worksheet:
        st.subheader("📝 Worksheet Generator")

        chapter = st.text_input("Enter chapter/topic")
        count = st.slider("Number of questions", 5, 30, 10)

        if st.button("Generate Worksheet"):
            if chapter.strip():
                with st.spinner("Generating worksheet..."):
                    qs = generate_questions(chapter, count)

                for i, q in enumerate(qs, start=1):
                    question_text = q.get("question", "")
                    answer_text = q.get("answer", "")

                    st.markdown(f"**Q{i}. {question_text}**")

                    with st.expander("Show Answer"):
                        st.write(answer_text)
            else:
                st.warning("Please enter a chapter/topic.")

    # Chapter Notes
    with tab_notes:
        st.subheader("📘 Chapter Notes Generator")

        text = st.text_area("Paste chapter text")

        if st.button("Generate Notes"):
            if text.strip():
                with st.spinner("Generating notes..."):
                    notes = summarize_chapter(text)

                st.subheader("Summary")
                st.write(notes)
            else:
                st.warning("Please paste chapter text.")
