import streamlit as st

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
# QUIZ CHAPTERS
# ---------------------------------------------------------
def render_quiz_chapters() -> None:
    require_user()  # user validation only
    sb = get_supabase()

    try:
        res = (
            sb.table("chapters")
            .select("id, grade, board, chapter_key, chapter_name")
            .order("grade", desc=True)
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

    require_user()
    require_student()

    # ---------------------------------------------------------
    # LOGOUT HANDLER
    # ---------------------------------------------------------
    params = st.query_params
    if params.get("student_logout") == "true":
        logout()
        return

    # ---------------------------------------------------------
    # TOP BAR
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

    # ---------------------------------------------------------
    # TABS
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # DASHBOARD TAB
    # ---------------------------------------------------------
    with tab_dashboard:
        render_dashboard()

    # ---------------------------------------------------------
    # CHAPTERS TAB
    # ---------------------------------------------------------
    with tab_chapters:
        render_chapters_page()

    # ---------------------------------------------------------
    # QUIZ TAB
    # ---------------------------------------------------------
    with tab_quiz:
        render_quiz_chapters()

    # ---------------------------------------------------------
    # SUBSCRIPTION TAB
    # ---------------------------------------------------------
    with tab_subs:
        render_subscriptions_page()

    # ---------------------------------------------------------
    # BILLING TAB
    # ---------------------------------------------------------
    with tab_billing:
        render_billing_history()

    # ---------------------------------------------------------
    # PUBLIC CONTENT TAB
    # ---------------------------------------------------------
    with tab_public:
        render_public_content()

    # ---------------------------------------------------------
    # AI TUTOR TAB
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # WORKSHEET GENERATOR TAB
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # CHAPTER NOTES TAB
    # ---------------------------------------------------------
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
