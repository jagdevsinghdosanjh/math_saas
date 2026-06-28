import streamlit as st
import re
from typing import Any, Dict, List, cast
from utils.db import get_supabase

TEXT_MUTED = "#a0a6b1"
TEXT_MAIN = "#f8f9fa"
ACCENT = "#00ff88"


# ------------------------------------------------------------
# GLOBAL STYLE
# ------------------------------------------------------------
def app_container_style() -> None:
    st.markdown(
        """<style>
        body {
            background: radial-gradient(circle at 20% 20%, #0f1115, #050608 60%);
            color: #f8f9fa;
            font-family: 'Inter', sans-serif;
        }
        .neon-card {
            background: rgba(18, 20, 23, 0.65);
            backdrop-filter: blur(12px);
            border-radius: 14px;
            padding: 20px;
            border: 1px solid rgba(0,255,136,0.25);
            box-shadow: 0 0 22px rgba(0,255,136,0.18);
        }
        h1, h2, h3, h4 {
            color: #00ff88;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# SANITIZERS
# ------------------------------------------------------------
def sanitize_html(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = re.sub(r"</?div[^>]*>", "", text, flags=re.IGNORECASE)
    return text.replace("&nbsp;", " ").strip()


def clean_math(text: Any) -> str:
    if not isinstance(text, str):
        return ""
    text = text.replace("\\\\(", "\\(").replace("\\\\)", "\\)")
    text = text.replace("\\\\[", "\\[").replace("\\\\]", "\\]")
    text = text.replace("\\\\frac", "\\frac")
    return re.sub(r"\$\s*\$", "$$", text)


# ------------------------------------------------------------
# PUBLIC CONTENT
# ------------------------------------------------------------
def render_public_content() -> None:
    sb = get_supabase()
    res = (
        sb.table("public_content")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    raw_items = getattr(res, "data", []) or []
    items: List[Dict[str, Any]] = [
        cast(Dict[str, Any], row) for row in raw_items if isinstance(row, dict)
    ]

    if not items:
        st.info("No public content available.")
        return

    for item in items:
        title = str(item.get("title", "Untitled"))
        body_raw = item.get("body", "")
        body = sanitize_html(clean_math(body_raw))

        st.markdown(f"### {title}")
        st.markdown(body, unsafe_allow_html=True)


# ------------------------------------------------------------
# DISPLAY NAME HANDLER (Fix for Pydantic User)
# ------------------------------------------------------------
def get_display_name(user: Any, role: str) -> str:
    # Case 1: dict (from profiles table)
    if isinstance(user, dict):
        return (
            user.get("full_name")
            or user.get("name")
            or user.get("email")
            or role.capitalize()
        )

    # Case 2: Supabase User object (Pydantic)
    meta = getattr(user, "user_metadata", {}) or {}
    email = getattr(user, "email", None)

    return (
        meta.get("full_name")
        or meta.get("name")
        or email
        or role.capitalize()
    )


# ------------------------------------------------------------
# TOP BAR (Refactored)
# ------------------------------------------------------------
def top_bar(title: str, role: str, logout_param: str) -> None:
    user = st.session_state.get("user")
    display_name = get_display_name(user, role)

    st.markdown(
        f"""
        <div style="background:#0a0c10; border-bottom:1px solid #00ff88; padding:12px 16px;">
            <span style="color:#00ff88; font-weight:600;">{display_name}</span>
            <h3 style="margin:4px 0 0 0; color:white;">{title}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Logout", key=f"logout_{role}"):
        logout()


# ------------------------------------------------------------
# LOGIN STATE STORAGE
# ------------------------------------------------------------
def set_logged_in_user(profile, role, access_token, refresh_token):
    """Store user, role, and Supabase session tokens."""
    st.session_state["user"] = profile
    st.session_state["role"] = role
    st.session_state["access_token"] = access_token
    st.session_state["refresh_token"] = refresh_token

    st.session_state["auth_state"] = {
        "user": profile,
        "role": role,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

    sb = get_supabase()
    st.session_state["session"] = sb.auth.get_session()


# ------------------------------------------------------------
# SESSION RESTORE (Refactored)
# ------------------------------------------------------------
def restore_session():
    sb = get_supabase()

    # 1. Restore from Supabase cookies
    session = sb.auth.get_session()
    if session and session.user:
        st.session_state["session"] = session
        st.session_state["user"] = session.user

        # Only set role if metadata contains it
        meta = session.user.user_metadata or {}
        if "role" in meta:
            st.session_state["role"] = meta["role"]

        st.session_state["access_token"] = session.access_token
        st.session_state["refresh_token"] = session.refresh_token

        return True

    # 2. Restore from stored auth_state
    auth_state = st.session_state.get("auth_state")
    if auth_state:
        st.session_state["user"] = auth_state.get("user")
        st.session_state["role"] = auth_state.get("role")

        access = auth_state.get("access_token")
        refresh = auth_state.get("refresh_token")

        if access and refresh:
            sb.auth.set_session(access, refresh)

        return True

    return False


# ------------------------------------------------------------
# LOGOUT
# ------------------------------------------------------------
def logout() -> None:
    try:
        sb = get_supabase()
        sb.auth.sign_out()
    except Exception:
        pass

    for key in [
        "user",
        "role",
        "jwt",
        "login_mode",
        "session",
        "auth_state",
        "access_token",
        "refresh_token",
    ]:
        st.session_state.pop(key, None)

    st.query_params.clear()
    st.rerun()


# ------------------------------------------------------------
# ROLE HELPERS
# ------------------------------------------------------------
def require_admin() -> None:
    if st.session_state.get("role") != "admin":
        st.error("Please login as admin.")
        st.stop()


def require_student() -> None:
    if st.session_state.get("role") != "student":
        st.error("Please login as student.")
        st.stop()
