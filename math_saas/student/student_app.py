import streamlit as st
from math_saas.auth import require_student
from math_saas.utils.db import get_supabase
from math_saas.student.subscriptions_page import render_subscriptions_page


def render_chapters():
    """Load and display published chapters."""
    supabase = get_supabase()

    res = (
        supabase.table("chapters")
        .select("title, slug, description")
        .eq("is_published", True)
        .order("created_at", asc=True)
        .execute()
    )

    chapters = res.data or []

    if not chapters:
        st.info("No chapters available yet.")
        return

    for ch in chapters:
        with st.expander(ch["title"]):
            st.write(ch.get("description") or "")


def run_student():
    """Main student portal with tabs."""
    require_student()

    st.title("Student Portal")

    tab_dashboard, tab_chapters, tab_subs = st.tabs(
        ["Dashboard", "Chapters", "Subscription"]
    )

    # -------------------------
    # Dashboard (simple version)
    # -------------------------
    with tab_dashboard:
        student = st.session_state.get("student")
        st.subheader("Welcome!")
        st.write(f"Logged in as: **{student['email']}**")

        st.info("Your learning dashboard will appear here soon.")

    # -------------------------
    # Chapters
    # -------------------------
    with tab_chapters:
        render_chapters()

    # -------------------------
    # Subscription Page
    # -------------------------
    with tab_subs:
        render_subscriptions_page()
