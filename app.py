import streamlit as st

from math_saas.auth import (
    logout,
    apply_dark_theme,
    apply_light_theme,
    restore_session,
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
    session = getattr(res, "session", None)

    if not user or not session or not getattr(session, "access_token", None):
        st.error("Invalid login credentials")
        return None, None

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
        return None, None

    if not isinstance(profile_raw, dict):
        st.error("Profile not found.")
        return None, None

    profile = profile_raw

    if role == "admin" and not profile.get("is_admin", False):
        st.error("You are not an admin.")
        return None, None

    if role == "student" and profile.get("is_admin", False):
        st.error("Students must login from Student Login.")
        return None, None

    # FINAL FIX — correct JWT extraction
    return profile, session.access_token



# -------------------------------------------------
# ADMIN LOGIN FORM
# -------------------------------------------------
def admin_login_form():
    st.markdown("<h3>Admin Login</h3>", unsafe_allow_html=True)
    email = st.text_input("Email", key="admin_email")
    password = st.text_input("Password", type="password", key="admin_password")

    if st.button("Login as Admin"):
        profile, jwt = handle_login(email, password, role="admin")
        if profile and jwt:
            set_logged_in_user(profile, role="admin", jwt=jwt)
            st.success("Admin login successful.")
            st.rerun()


# -------------------------------------------------
# STUDENT LOGIN FORM
# -------------------------------------------------
def student_login_form():
    st.markdown("<h3>Student Login</h3>", unsafe_allow_html=True)
    email = st.text_input("Email", key="student_email")
    password = st.text_input("Password", type="password", key="student_password")

    if st.button("Login as Student"):
        profile, jwt = handle_login(email, password, role="student")
        if profile and jwt:
            set_logged_in_user(profile, role="student", jwt=jwt)
            st.success("Student login successful.")
            st.rerun()


# -------------------------------------------------
# MAIN ROUTER
# -------------------------------------------------
def main():
    # Restore persistent session (URL token → session_state)
    restore_session()

    # -----------------------------
    # THEME SELECTION (GLOBAL)
    # -----------------------------
    theme_choice = st.radio(
        "Choose Theme:",
        ["Dark (Neon)", "Light"],
        horizontal=True,
        key="theme_choice_radio",
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
        if st.button("Admin Login", key="btn_admin_login"):
            st.session_state["login_mode"] = "admin"
            st.rerun()

    with col2:
        if st.button("Student Login", key="btn_student_login"):
            st.session_state["login_mode"] = "student"
            st.rerun()

    with col3:
        if st.button("New Student? Sign Up", key="btn_signup"):
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
