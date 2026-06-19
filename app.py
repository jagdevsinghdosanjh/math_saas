import streamlit as st
from typing import Dict

from auth import (
    restore_session,
    logout,
    apply_dark_theme,
    apply_light_theme,
    set_logged_in_user,
)
from admin.admin_app import run_admin
from student.student_app import run_student
from student.public_content import render_public_content
from student.signup_page import render_signup_page
from utils.db import get_supabase


# -------------------------------------------------
# GENERIC LOGIN HANDLER
# -------------------------------------------------
def handle_login(email: str, password: str, role: str):
    sb = get_supabase()

    try:
        res = sb.auth.sign_in_with_password({"email": email, "password": password})
    except Exception:
        st.error("Invalid login credentials")
        return None, None

    user = res.user
    session = res.session

    if not user or not session or not session.access_token:
        st.error("Invalid login credentials")
        return None, None

    # Fetch profile
    profile_raw = (
        sb.table("profiles")
        .select("*")
        .eq("id", user.id)
        .single()
        .execute()
        .data
    )

    if not isinstance(profile_raw, dict):
        st.error("Profile not found.")
        return None, None

    # Role validation
    if role == "admin" and not profile_raw.get("is_admin", False):
        st.error("You are not an admin.")
        return None, None

    if role == "student" and profile_raw.get("is_admin", False):
        st.error("Students must login from Student Login.")
        return None, None

    return profile_raw, session


# -------------------------------------------------
# ADMIN LOGIN FORM
# -------------------------------------------------
def admin_login_form():
    st.markdown("<h3>Admin Login</h3>", unsafe_allow_html=True)
    email = st.text_input("Email", key="admin_email")
    password = st.text_input("Password", type="password", key="admin_pass")

    if st.button("Login as Admin"):
        profile, session = handle_login(email, password, "admin")
        if profile and session:
            st.session_state["session"] = session
            set_logged_in_user(profile, "admin", session.access_token)
            st.rerun()


# -------------------------------------------------
# STUDENT LOGIN FORM
# -------------------------------------------------
def student_login_form():
    st.markdown("<h3>Student Login</h3>", unsafe_allow_html=True)
    email = st.text_input("Email", key="student_email")
    password = st.text_input("Password", type="password", key="student_pass")

    if st.button("Login as Student"):
        profile, session = handle_login(email, password, "student")
        if profile and session:
            st.session_state["session"] = session

            # REQUIRED FIX
            st.session_state["student"] = profile
            st.session_state["user"] = profile   # <-- THIS LINE FIXES EVERYTHING

            set_logged_in_user(profile, "student", session.access_token)
            st.rerun()
# def student_login_form():
#     st.markdown("<h3>Student Login</h3>", unsafe_allow_html=True)
#     email = st.text_input("Email", key="student_email")
#     password = st.text_input("Password", type="password", key="student_pass")

#     if st.button("Login as Student"):
#         profile, session = handle_login(email, password, "student")
#         if profile and session:
#             st.session_state["session"] = session
#             set_logged_in_user(profile, "student", session.access_token)
#             st.rerun()


# -------------------------------------------------
# MAIN ROUTER
# -------------------------------------------------
def main():
    # Restore Supabase session (if exists)
    restore_session()

    # Theme
    theme_choice = st.radio(
        "Choose Theme:",
        ["Dark (Neon)", "Light"],
        horizontal=True,
    )

    if theme_choice == "Light":
        apply_light_theme()
    else:
        apply_dark_theme()

    # -----------------------------
    # AUTH ROUTING
    # -----------------------------
    role = st.session_state.get("role")

    if role == "admin":
        run_admin()
        return

    if role == "student":
        run_student()
        return

    # -----------------------------
    # LOGIN GATEWAY
    # -----------------------------
    st.markdown("<h2>Welcome to Student's Math Companion</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Admin Login"):
            st.session_state["login_mode"] = "admin"
            st.rerun()

    with col2:
        if st.button("Student Login"):
            st.session_state["login_mode"] = "student"
            st.rerun()

    with col3:
        if st.button("New Student? Sign Up"):
            st.session_state["login_mode"] = "signup"
            st.rerun()

    mode = st.session_state.get("login_mode")

    if mode == "admin":
        admin_login_form()
    elif mode == "student":
        student_login_form()
    elif mode == "signup":
        render_signup_page()

    st.markdown("<hr>", unsafe_allow_html=True)
    render_public_content()


if __name__ == "__main__":
    main()
