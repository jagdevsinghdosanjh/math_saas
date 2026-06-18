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
        """
        <style>
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
        .neon-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 0 28px rgba(0,255,136,0.35);
        }
        h1, h2, h3, h4 {
            color: #00ff88;
            font-weight: 600;
        }
        p {
            color: #b5b8c2;
        }
        .stButton>button {
            background: linear-gradient(135deg, #00ff88, #00cc6a);
            color: black;
            border-radius: 8px;
            padding: 8px 18px;
            border: none;
            font-weight: 600;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #00ffaa, #00dd77);
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
    res = sb.table("public_content").select("*").order("created_at", desc=True).execute()
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
# THEMES
# ------------------------------------------------------------
def apply_dark_theme() -> None:
    st.markdown(
        """
        <style>.main { background: #050608; color: #f8f9fa; }</style>
        """,
        unsafe_allow_html=True,
    )


def apply_light_theme() -> None:
    st.markdown(
        """
        <style>.main { background: #ffffff; color: #111827; }</style>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# TOP BAR
# ------------------------------------------------------------
def top_bar(title: str, role: str, logout_param: str) -> None:
    """
    Uses unified session model: session_state["user"], session_state["role"]
    Falls back to old per-role keys if needed.
    """
    user: Dict[str, Any] = {}

    if st.session_state.get("role") == role and isinstance(st.session_state.get("user"), dict):
        user = st.session_state["user"]
    else:
        maybe_user = st.session_state.get(role, {})
        if isinstance(maybe_user, dict):
            user = maybe_user

    display_name = user.get("full_name") or user.get("name") or role.capitalize()

    st.markdown(
        f"""
        <div style="background:#0a0c10; border-bottom:1px solid #00ff88; padding:12px 16px;">
            <span style="color:#00ff88; font-weight:600;">{display_name}</span>
            <h3 style="margin:4px 0 0 0; color:white;">{title}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    from auth import logout as _logout

    if st.button("Logout", key=f"logout_{role}"):
        _logout()


# ------------------------------------------------------------
# AUTH PERSISTENCE (SAFE)
# ------------------------------------------------------------
def set_logged_in_user(user: Dict[str, Any], role: str, jwt: str) -> None:
    """
    Secure login: session-only, no URL tokens.
    """
    st.session_state.clear()
    st.session_state["user"] = user
    st.session_state["role"] = role
    st.session_state["jwt"] = jwt

    # backward compatibility
    st.session_state[role] = user


def restore_session() -> None:
    """
    No auto-login from URL. Only use session_state.
    """
    return


# ------------------------------------------------------------
# LOGOUT
# ------------------------------------------------------------
def logout() -> None:
    for key in ["user", "role", "jwt", "student", "admin", "login_mode"]:
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
