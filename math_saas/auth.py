import streamlit as st
import re
from typing import Any, Dict, List, cast
from math_saas.utils.db import get_supabase

TEXT_MUTED = "#a0a6b1"
TEXT_MAIN = "#f8f9fa"
ACCENT = "#00ff88"


# ------------------------------------------------------------
# GLOBAL STYLE
# ------------------------------------------------------------
def app_container_style() -> None:
    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(135deg, #050608 0%, #0a0c10 100%);
            color: #f8f9fa;
            font-family: 'Inter', sans-serif;
        }
        .neon-card {
            background: #121417;
            border-radius: 14px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 0 18px rgba(0,255,136,0.25);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# CLEAN MATH
# ------------------------------------------------------------
def clean_math(text: Any) -> str:
    if not isinstance(text, str):
        return ""
    text = text.replace("\\\\(", "\\(").replace("\\\\)", "\\)")
    text = text.replace("\\\

\[", "\

\[").replace("\\\\]

", "\\]

")
    text = text.replace("\\\\frac", "\\frac")
    return re.sub(r"\$\s*\$", "$$", text)


# ------------------------------------------------------------
# PUBLIC CONTENT
# ------------------------------------------------------------
def render_public_content() -> None:
    sb = get_supabase()
    res: Any = (
        sb.table("public_content")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    raw_items: Any = getattr(res, "data", []) or []

    items: List[Dict[str, Any]] = [
        cast(Dict[str, Any], row)
        for row in raw_items
        if isinstance(row, dict)
    ]

    if not items:
        st.info("No public content available.")
        return

    for item in items:
        title: str = str(item.get("title", "Untitled"))
        body_raw: Any = item.get("body", "")
        body: str = clean_math(body_raw)

        st.markdown(f"### {title}")
        st.markdown(body, unsafe_allow_html=True)


# ------------------------------------------------------------
# THEMES
# ------------------------------------------------------------
def apply_dark_theme() -> None:
    st.markdown(
        """
        <style>
        .main { background: #050608; color: #f8f9fa; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def apply_light_theme() -> None:
    st.markdown(
        """
        <style>
        .main { background: #ffffff; color: #111827; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# TOP BAR
# ------------------------------------------------------------
def top_bar(title: str, role: str, logout_param: str) -> None:
    st.markdown(
        f"""
        <div style="padding:12px; background:#0a0c10; border-bottom:1px solid #00ff88;">
            <span style="color:#00ff88; font-weight:600;">{role}</span>
            <h3 style="margin:4px 0 0 0;">{title}</h3>
            <a href="/?{logout_param}=true"
               style="float:right; background:#ff4d6d; padding:8px 16px; border-radius:8px; color:white;">
               Logout
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# AUTH PERSISTENCE
# ------------------------------------------------------------
def set_logged_in_user(user: Dict[str, Any], role: str, jwt: str) -> None:
    st.session_state[role] = user
    st.session_state["jwt"] = jwt

    # Store token + role in URL
    st.query_params = {"token": jwt, "role": role}


def restore_session() -> None:
    """
    Restores a logged-in session using token + role stored in query params.
    Prevents auto-login after logout and avoids Streamlit Cloud session issues.
    """

    raw_params = st.query_params
    params: Dict[str, str] = dict(raw_params) if isinstance(raw_params, dict) else {}

    # 1. Prevent auto-login after logout
    if params.get("student_logout") == "true" or params.get("admin_logout") == "true":
        return

    # 2. Extract token + role
    token = params.get("token")
    role = params.get("role")

    if not token or not role:
        return

    # 3. If already logged in, skip
    if "student" in st.session_state or "admin" in st.session_state:
        return

    # 4. Validate token with Supabase
    sb = get_supabase()
    try:
        user_resp = sb.auth.get_user(token)
    except Exception:
        return

    user = getattr(user_resp, "user", None)
    if not user:
        return

    # 5. Restore session
    st.session_state["jwt"] = token
    st.session_state[role] = user


# ------------------------------------------------------------
# LOGOUT (FINAL FIXED VERSION)
# ------------------------------------------------------------
def logout() -> None:
    """
    Clears only authentication-related session keys,
    clears query params, and forces a clean rerun.
    """

    keys_to_clear = [
        "student",
        "admin",
        "role",
        "jwt",
        "authenticated",
        "login_mode",
    ]

    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

    # Clear URL params
    st.query_params.clear()

    # Force clean rerun
    st.rerun()


# ------------------------------------------------------------
# ROLE HELPERS
# ------------------------------------------------------------
def require_admin() -> None:
    if "admin" not in st.session_state:
        st.error("Please login as admin.")
        st.stop()


def require_student() -> None:
    if "student" not in st.session_state:
        st.error("Please login as student.")
        st.stop()
