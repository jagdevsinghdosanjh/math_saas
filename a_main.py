import streamlit as st
from auth import logout, apply_dark_theme, apply_light_theme
from admin.admin_app import run_admin
from student.student_app import run_student
from student.public_content import render_public_content
from utils.db import get_supabase

# ---------------------------------------------------------
# GENERIC LOGIN HANDLER
# ---------------------------------------------------------
def handle_login(email, password, role):
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


# ---------------------------------------------------------
# ADMIN LOGIN FORM
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# STUDENT LOGIN FORM
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# MAIN APP (NEW UI + OLD WORKING LOGIN LOGIC)
# ---------------------------------------------------------
def main():

    # --------------------------
    # THEME SELECTOR
    # --------------------------
    theme_choice = st.radio(
        "Choose Theme:",
        ["Dark (Neon)", "Light"],
        horizontal=True
    )

    if theme_choice == "Light":
        apply_light_theme()
    else:
        apply_dark_theme()

    # --------------------------
    # LOGOUT HANDLING
    # --------------------------
    params = st.query_params
    if params.get("admin_logout") == "true":
        logout()
    if params.get("student_logout") == "true":
        logout()

    # --------------------------
    # SESSION ROUTING
    # --------------------------
    admin_data = st.session_state.get("admin")
    student_data = st.session_state.get("student")

    if isinstance(admin_data, dict):
        run_admin()
        return

    if isinstance(student_data, dict):
        run_student()
        return

    # --------------------------
    # NEW LANDING PAGE UI
    # --------------------------
    st.markdown(
        """
        <div style="padding-top:1rem;">
            <h1 style="color:white; font-size:2.4rem; font-weight:800;">Math Hub</h1>
            <p style="color:#9ca3af; margin-top:-10px;">Research‑grade math workspace</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="margin-top:1rem;">
            <span style="
                display:inline-block;
                padding:4px 10px;
                border-radius:999px;
                background:rgba(59,130,246,0.12);
                border:1px solid rgba(59,130,246,0.4);
                color:#93c5fd;
                font-size:0.75rem;
                letter-spacing:0.06em;
                text-transform:uppercase;">
                For serious learners & educators
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h2 style="color:white; font-size:2rem; font-weight:700; margin-top:0.8rem;">
            The research‑grade workspace<br>for school & competitive math.
        </h2>
        <p style="color:#d1d5db; font-size:1rem;">
            Powered by structured chapter maps, daily math posts, and curated problem sets for Boards & JEE.
        </p>
        """,
        unsafe_allow_html=True
    )

    # --------------------------
    # LOGIN BUTTONS
    # --------------------------
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Admin Login", width="stretch"):
            st.session_state["login_mode"] = "admin"
            st.rerun()

    with col2:
        if st.button("Student Login", width="stretch"):
            st.session_state["login_mode"] = "student"
            st.rerun()

    mode = st.session_state.get("login_mode")

    if mode == "admin":
        admin_login_form()
    elif mode == "student":
        student_login_form()

    # --------------------------
    # PUBLIC CONTENT ALWAYS VISIBLE
    # --------------------------
    st.markdown("<hr>", unsafe_allow_html=True)
    render_public_content()


if __name__ == "__main__":
    main()
