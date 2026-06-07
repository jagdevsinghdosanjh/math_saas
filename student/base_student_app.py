﻿import streamlit as st
from typing import Any, Dict, List

from auth import require_student
from utils.db import get_supabase
from student.subscriptions_page import render_subscriptions_page
from subscriptions.access import require_active_subscription

from student.billing_history import render_billing_history

# in run_student()
tab_dashboard, tab_chapters, tab_subs, tab_billing = st.tabs(
    ["Dashboard", "Chapters", "Subscription", "Billing"]
)

with tab_billing:
    render_billing_history()


# -----------------------------
# Render Chapters List
# -----------------------------
def render_chapters():
    sb = get_supabase()

    res = (
        sb.table("chapters")
        .select("id, title, slug, description, is_premium, is_published")
        .eq("is_published", True)
        .order("created_at", asc=True)
        .execute()
    )

    raw = res.data or []
    chapters: List[Dict[str, Any]] = [
        item for item in raw if isinstance(item, dict)
    ]

    if not chapters:
        st.info("No chapters available yet.")
        return

    for ch in chapters:
        title = ch.get("title", "Untitled")
        desc = ch.get("description", "")
        is_premium = ch.get("is_premium", False)

        with st.expander(title):

            # Premium content lock
            if is_premium:
                st.warning("This is premium content.")
                require_active_subscription()

            st.write(desc)


# -----------------------------
# Dashboard (Simple Version)
# -----------------------------
def render_dashboard():
    student = st.session_state.get("student")

    st.subheader("Welcome!")
    st.write(f"Logged in as: **{student.get('email', '')}**")

    st.info("Your learning dashboard will appear here soon.")



# -----------------------------
# Main Student Portal
# -----------------------------
def run_student():
    require_student()

    st.title("Student Portal")

    student = st.session_state.get("student")
    if not student:
        st.error("Student session missing. Please login again.")
        st.stop()

    tab_dashboard, tab_chapters, tab_subs = st.tabs(
        ["Dashboard", "Chapters", "Subscription"]
    )

    with tab_dashboard:
        render_dashboard()

    with tab_chapters:
        render_chapters()

    with tab_subs:
        render_subscriptions_page()

# import streamlit as st
# from math_saas.auth import require_student
# from math_saas.utils.db import get_supabase
# from math_saas.student.subscriptions_page import render_subscriptions_page


# def render_chapters():
#     """Load and display published chapters."""
#     supabase = get_supabase()

#     res = (
#         supabase.table("chapters")
#         .select("title, slug, description")
#         .eq("is_published", True)
#         .order("created_at", asc=True)
#         .execute()
#     )

#     chapters = res.data or []

#     if not chapters:
#         st.info("No chapters available yet.")
#         return

#     for ch in chapters:
#         with st.expander(ch["title"]):
#             st.write(ch.get("description") or "")


# def run_student():
#     """Main student portal with tabs."""
#     require_student()

#     st.title("Student Portal")

#     tab_dashboard, tab_chapters, tab_subs = st.tabs(
#         ["Dashboard", "Chapters", "Subscription"]
#     )

#     # -------------------------
#     # Dashboard (simple version)
#     # -------------------------
#     with tab_dashboard:
#         student = st.session_state.get("student")
#         st.subheader("Welcome!")
#         st.write(f"Logged in as: **{student['email']}**")

#         st.info("Your learning dashboard will appear here soon.")

#     # -------------------------
#     # Chapters
#     # -------------------------
#     with tab_chapters:
#         render_chapters()

#     # -------------------------
#     # Subscription Page
#     # -------------------------
#     with tab_subs:
#         render_subscriptions_page()
