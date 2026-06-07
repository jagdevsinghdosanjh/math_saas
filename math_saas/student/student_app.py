import streamlit as st
from math_saas.student.public_content import render_public_content
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
from math_saas.utils.db import get_supabase


# -----------------------------
# NEW: Synced Chapters Renderer
# -----------------------------
import streamlit as st
from math_saas.utils.db import get_supabase


def render_synced_chapters():
    """Display synced chapters from Supabase sync_chapters table safely, with quiz links."""
    sb = get_supabase()
    try:
        res = sb.table("sync_chapters").select("*").eq("is_published", True).order("created_at", desc=True).execute()
        chapters = res.data or []
    except Exception as e:
        st.error(f"Error fetching chapters: {e}")
        return

    if not chapters:
        st.info("No synced chapters available yet.")
        return

    st.subheader("📘 Synced Chapters (CBSE 9th Math)")

    for ch in chapters:
        if not isinstance(ch, dict):
            continue

        title = str(ch.get("chapter_title", "Untitled"))
        desc = str(ch.get("description", "Chapter details coming soon."))
        url = ch.get("chapter_url")

        with st.expander(title):
            st.write(desc)
            if isinstance(url, str) and url.strip():
                st.markdown(f"[View Chapter]({url})", unsafe_allow_html=True)

            # ✅ Add “Start Quiz” button
            quiz_url = f"https://quiz-byjsdasr1973.streamlit.app/?chapter={title.replace(' ', '%20')}"
            if st.button(f"Start Quiz for {title}", key=f"quiz_{title}"):
                st.markdown(f'<a href="{quiz_url}" target="_blank"><button>Start Quiz</button></a>', unsafe_allow_html=True)
                # st.markdown(f"[Open Quiz Portal]({quiz_url})", unsafe_allow_html=True)


# -----------------------------
# STUDENT PORTAL MAIN FUNCTION
# -----------------------------
def run_student():
    app_container_style()

    # Safe query param access
    params = st.query_params
    if params.get("student_logout") == "true":
        logout()

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

    TAB_LABELS = ["Dashboard", "Chapters", "Subscription", "Billing", "Math & News"]
    tab_dashboard, tab_chapters, tab_subs, tab_billing, tab_public = st.tabs(TAB_LABELS)

    # Routing dictionary for cleaner logic
    ROUTES = {
        "Dashboard": render_dashboard,
        "Chapters": render_chapters_page,
        "Subscription": render_subscriptions_page,
        "Billing": render_billing_history,
        "Math & News": render_public_content,
    }

    # Dashboard
    with tab_dashboard:
        try:
            ROUTES["Dashboard"]()
        except Exception:
            st.info("Dashboard coming soon.")

    # Chapters
    with tab_chapters:
        try:
            ROUTES["Chapters"]()
            st.markdown("---")
            render_synced_chapters()  # ✅ Added new synced chapters section
        except Exception:
            st.info("Chapters page coming soon.")

    # Subscription
    with tab_subs:
        ROUTES["Subscription"]()

    # Billing
    with tab_billing:
        ROUTES["Billing"]()

    # Public content
    with tab_public:
        ROUTES["Math & News"]()
