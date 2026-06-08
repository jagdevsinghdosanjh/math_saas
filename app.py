import streamlit as st

from math_saas.auth import (
    logout,
    apply_dark_theme,
    apply_light_theme,
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
        return None

    user = res.user
    if not user:
        st.error("Invalid login credentials")
        return None

    # Fetch profile
    try:
        profile_raw = (
            sb.table("profiles")
            .select("*")
            .eq("id", user.id)
            .single()
            .execute()
            .data
        )
    except Exception:
        st.error("Profile not found or RLS blocked access.")
        return None

    profile = profile_raw if isinstance(profile_raw, dict) else None
    if not profile:
        st.error("Profile not found.")
        return None

    # Role validation
    if role == "admin" and not profile.get("is_admin", False):
        st.error("You are not an admin.")
        return None

    if role == "student" and profile.get("is_admin", False):
        st.error("Students must login from Student Login.")
        return None

    return profile


# -------------------------------------------------
# ADMIN LOGIN FORM
# -------------------------------------------------
def admin_login_form():
    st.markdown("<h3>Admin Login</h3>", unsafe_allow_html=True)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login as Admin"):
        profile = handle_login(email, password, role="admin")
        if profile:
            st.session_state["admin"] = profile
            st.success("Admin login successful.")
            st.rerun()


# -------------------------------------------------
# STUDENT LOGIN FORM
# -------------------------------------------------
def student_login_form():
    st.markdown("<h3>Student Login</h3>", unsafe_allow_html=True)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login as Student"):
        profile = handle_login(email, password, role="student")
        if profile:
            st.session_state["student"] = profile
            st.success("Student login successful.")
            st.rerun()


# -------------------------------------------------
# MAIN ROUTER
# -------------------------------------------------
def main():
    # -----------------------------
    # THEME SELECTION (GLOBAL)
    # -----------------------------
    theme_choice = st.radio(
        "Choose Theme:",
        ["Dark (Neon)", "Light"],
        horizontal=True
    )

    st.session_state["theme_choice"] = theme_choice

    if theme_choice == "Light":
        apply_light_theme()
    else:
        apply_dark_theme()

    # -----------------------------
    # LOGOUT HANDLING
    # -----------------------------
    params = st.query_params
    if params.get("admin_logout") == "true":
        logout()
    if params.get("student_logout") == "true":
        logout()

    # -----------------------------
    # ROUTE TO DASHBOARDS
    # -----------------------------
    admin_data = st.session_state.get("admin")
    student_data = st.session_state.get("student")

    if isinstance(admin_data, dict):
        run_admin()
        return

    if isinstance(student_data, dict):
        run_student()
        return

    # -----------------------------
    # LOGIN / SIGNUP GATEWAY
    # -----------------------------
    st.markdown(
        """
        <h2 style="margin-top:0;">Welcome to Student's Math Companion</h2>
        <p style="color:#9ca3af;">Choose your login type to continue.</p>
        """,
        unsafe_allow_html=True,
    )

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

    # -----------------------------
    # PUBLIC CONTENT ALWAYS VISIBLE
    # -----------------------------
    st.markdown("<hr>", unsafe_allow_html=True)
    render_public_content()


if __name__ == "__main__":
    main()
