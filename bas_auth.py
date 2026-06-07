﻿import streamlit as st
from typing import Optional, TypedDict, cast
from utils.db import get_supabase


# -----------------------------
# Typed Profile Structure
# -----------------------------
class Profile(TypedDict, total=False):
    id: str
    email: str
    is_admin: bool


# -----------------------------
# ADMIN LOGIN
# -----------------------------
def admin_login_form():
    st.subheader("Admin Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login", type="primary"):
        sb = get_supabase()

        try:
            res = sb.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
        except Exception:
            st.error("Invalid login credentials")
            return

        user = res.user
        if not user:
            st.error("Invalid login credentials")
            return

        # Fetch profile
        result = (
            sb.table("profiles")
            .select("id, email, is_admin")
            .eq("id", user.id)
            .single()
            .execute()
        )

        profile = cast(Optional[Profile], result.data)

        if not profile:
            st.error("Profile not found in database")
            return

        if not profile.get("is_admin"):
            st.error("You are not authorized as admin")
            return

        # Store session
        st.session_state["user"] = profile
        st.session_state["is_admin"] = True

        st.success("Logged in successfully")
        st.rerun()


def require_admin():
    """Protect admin pages."""
    if st.session_state.get("is_admin"):
        return
    admin_login_form()
    st.stop()


# -----------------------------
# STUDENT LOGIN
# -----------------------------
def student_login_form():
    st.subheader("Student Login")

    email = st.text_input("Email", key="student_email")
    password = st.text_input("Password", type="password", key="student_pass")

    if st.button("Login", type="primary", key="student_login_btn"):
        sb = get_supabase()

        try:
            res = sb.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
        except Exception:
            st.error("Invalid login credentials")
            return

        user = res.user
        if not user:
            st.error("Invalid login credentials")
            return

        # Fetch profile
        result = (
            sb.table("profiles")
            .select("id, email, is_admin")
            .eq("id", user.id)
            .single()
            .execute()
        )

        profile = cast(Optional[Profile], result.data)

        if not profile:
            st.error("Profile not found")
            return

        if profile.get("is_admin"):
            st.error("Admins must login from Admin tab")
            return

        # Store session
        st.session_state["student"] = profile
        st.session_state["is_student"] = True

        st.success("Logged in successfully")
        st.rerun()


def require_student():
    """Protect student pages."""
    if st.session_state.get("is_student"):
        return
    student_login_form()
    st.stop()


# -----------------------------
# LOGOUT
# -----------------------------
def logout():
    st.session_state.clear()
    st.success("Logged out successfully")
    st.rerun()
