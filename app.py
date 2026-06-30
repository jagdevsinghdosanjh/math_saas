import streamlit as st
import auth
import pages.razorpay_checkout as razorpay_checkout

from themes.theme import apply_dark_theme, apply_light_theme
from admin.admin_app import run_admin
from student.student_app import run_student
from student.public_content import render_public_content
from student.signup_page import render_signup_page
from utils.db import get_supabase

st.set_page_config(page_title="Math Hub", page_icon="📘", layout="wide")


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
            st.session_state["user"] = profile
            st.session_state["role"] = "admin"
            st.session_state["access_token"] = session.access_token
            st.session_state["refresh_token"] = session.refresh_token
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
            st.session_state["user"] = profile
            st.session_state["role"] = "student"
            st.session_state["access_token"] = session.access_token
            st.session_state["refresh_token"] = session.refresh_token
            st.rerun()


# -------------------------------------------------
# MAIN ROUTER
# -------------------------------------------------
def main():
    # Restore session FIRST
    auth.restore_session()

    # Prevent direct access to checkout without session
    if "user" not in st.session_state and st.query_params.get("page") == "razorpay_checkout":
        st.error("Session expired. Please log in again.")
        return

    # Razorpay redirect (same tab)
    if st.query_params.get("page") == "razorpay_checkout":
        razorpay_checkout.render_razorpay_checkout()
        return

    # -------------------------------------------------
    # THEME SELECTION (Refactored — No "None")
    # -------------------------------------------------

    # Ensure theme_choice is always valid
    if st.session_state.get("theme_choice") not in ["Dark (Neon)", "Light"]:
        st.session_state["theme_choice"] = "Dark (Neon)"

    default_theme = st.session_state["theme_choice"]

    theme_choice = st.radio(
        "Choose Theme:",
        ["Dark (Neon)", "Light"],
        index=["Dark (Neon)", "Light"].index(default_theme),
        horizontal=True,
    )

    st.session_state["theme_choice"] = theme_choice

    # Apply theme
    apply_light_theme() if theme_choice == "Light" else apply_dark_theme()

    # -------------------------------------------------
    # ROLE ROUTING
    # -------------------------------------------------
    role = st.session_state.get("role")

    if role == "admin":
        run_admin()
        return

    if role == "student":
        run_student()
        return

    # -------------------------------------------------
    # PUBLIC LANDING PAGE
    # -------------------------------------------------
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
