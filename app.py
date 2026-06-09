import streamlit as st
from typing import Dict

from math_saas.auth import (
    restore_session,
    logout,
    apply_dark_theme,
    apply_light_theme,
    set_logged_in_user,
)
from math_saas.admin.admin_app import run_admin
from math_saas.student.student_app import run_student
from math_saas.student.public_content import render_public_content
from math_saas.student.signup_page import render_signup_page
from math_saas.utils.db import get_supabase


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

    if role == "admin" and not profile_raw.get("is_admin", False):
        st.error("You are not an admin.")
        return None, None

    if role == "student" and profile_raw.get("is_admin", False):
        st.error("Students must login from Student Login.")
        return None, None

    return profile_raw, session.access_token


# -------------------------------------------------
# ADMIN LOGIN FORM
# -------------------------------------------------
def admin_login_form():
    st.markdown("<h3>Admin Login</h3>", unsafe_allow_html=True)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login as Admin"):
        profile, jwt = handle_login(email, password, "admin")
        if profile and isinstance(jwt, str):
            set_logged_in_user(profile, "admin", jwt)
            st.rerun()

# -------------------------------------------------
# STUDENT LOGIN FORM
# -------------------------------------------------
def student_login_form():
    st.markdown("<h3>Student Login</h3>", unsafe_allow_html=True)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login as Student"):
        profile, jwt = handle_login(email, password, "student")
        if profile and isinstance(jwt, str):
            set_logged_in_user(profile, "student", jwt)
            st.rerun()

# -------------------------------------------------
# MAIN ROUTER
# -------------------------------------------------
def main():
    # MUST BE FIRST LINE
    restore_session()

    theme_choice = st.radio(
        "Choose Theme:",
        ["Dark (Neon)", "Light"],
        horizontal=True,
    )

    if theme_choice == "Light":
        apply_light_theme()
    else:
        apply_dark_theme()

    params: Dict[str, str] = dict(st.query_params)

    if params.get("admin_logout") == "true":
        logout()
    if params.get("student_logout") == "true":
        logout()

    if "admin" in st.session_state:
        run_admin()
        return

    if "student" in st.session_state:
        run_student()
        return

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
