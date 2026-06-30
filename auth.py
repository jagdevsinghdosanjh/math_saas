import streamlit as st
import re
from typing import Any, Dict, List, cast

from utils.db import get_supabase
from themes.theme import is_dark_theme

# Required by admin_app.py
TEXT_MUTED = "#a0a6b1"
TEXT_MAIN = "#f8f9fa"
ACCENT = "#00ff88"


# ---------------------------------------------------------
# SAFE USER EXTRACTOR (DICT or SUPABASE USER OBJECT)
# ---------------------------------------------------------
def extract_user_dict(user_obj: Any) -> Dict[str, Any]:
    """
    Converts Supabase User object or dict into a clean dict.
    Ensures consistent access to fields like is_admin, email, metadata.
    """

    if isinstance(user_obj, dict):
        return user_obj

    # Supabase User object
    meta = getattr(user_obj, "user_metadata", {}) or {}
    email = getattr(user_obj, "email", None)

    return {
        "id": getattr(user_obj, "id", None),
        "email": email,
        "full_name": meta.get("full_name"),
        "name": meta.get("name"),
        "is_admin": meta.get("is_admin", False),
        "metadata": meta,
    }
def app_container_style() -> None:
    dark = is_dark_theme()

    if dark:
        bg = "radial-gradient(circle at 20% 20%, #0f1115, #050608 60%)"
        text = "#f8f9fa"
        card_bg = "rgba(18, 20, 23, 0.65)"
        card_border = "rgba(0,255,136,0.25)"
        card_shadow = "0 0 22px rgba(0,255,136,0.18)"
        accent = "#00ff88"
    else:
        bg = "#ffffff"
        text = "#222222"
        card_bg = "#fafafa"
        card_border = "#ddd"
        card_shadow = "0 0 12px rgba(0,0,0,0.08)"
        accent = "#009944"

    st.markdown(
        f"""
        <style>
        body, .stApp {{
            background: {bg} !important;
            color: {text} !important;
        }}

        p, span, label, h1, h2, h3, h4, h5, h6, div {{
            color: {text} !important;
        }}

        .neon-card, .app-card {{
            background: {card_bg} !important;
            border-radius: 14px;
            padding: 20px;
            border: 1px solid {card_border} !important;
            box-shadow: {card_shadow} !important;
        }}

        h1, h2, h3, h4 {{
            color: {accent} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# SESSION RESTORE (CRITICAL)
# ---------------------------------------------------------
def restore_session() -> bool:
    sb = get_supabase()

    # 1. Supabase cookie session
    session = sb.auth.get_session()
    if session and session.user:
        user_dict = extract_user_dict(session.user)

        st.session_state["auth_state"] = {
            "user": user_dict,
            "role": user_dict.get("metadata", {}).get("role"),
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
        }
        return True

    # 2. Stored session_state
    auth_state = st.session_state.get("auth_state")
    if auth_state:
        access = auth_state.get("access_token")
        refresh = auth_state.get("refresh_token")

        if access and refresh:
            sb.auth.set_session(access, refresh)

        return True

    return False


# ---------------------------------------------------------
# REQUIRE USER
# ---------------------------------------------------------
def require_user():
    auth_state = st.session_state.get("auth_state")
    if not auth_state:
        st.error("You are not logged in.")
        st.stop()

    return auth_state["user"]


# ---------------------------------------------------------
# REQUIRE STUDENT
# ---------------------------------------------------------
def require_student():
    user = require_user()

    if user.get("is_admin", False):
        st.error("Students only. Please use Admin Login.")
        st.stop()

    return user


# ---------------------------------------------------------
# REQUIRE ADMIN
# ---------------------------------------------------------
def require_admin():
    user = require_user()

    if not user.get("is_admin", False):
        st.error("Admin access required.")
        st.stop()

    return user


# ---------------------------------------------------------
# SANITIZERS
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# PUBLIC CONTENT
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# DISPLAY NAME
# ---------------------------------------------------------
def get_display_name(user: Any, role: str) -> str:
    # Handle None safely
    if not user:
        return role.capitalize()

    # If dict
    if isinstance(user, dict):
        return (
            user.get("full_name")
            or user.get("name")
            or user.get("email")
            or role.capitalize()
        )

    # If Supabase User object
    meta = getattr(user, "user_metadata", {}) or {}
    email = getattr(user, "email", None)

    return (
        meta.get("full_name")
        or meta.get("name")
        or email
        or role.capitalize()
    )

# ---------------------------------------------------------
# TOP BAR
# ---------------------------------------------------------
def top_bar(title: str, role: str) -> None:
    dark = is_dark_theme()

    if dark:
        bar_bg = "#0a0c10"
        bar_border = "#00ff88"
        name_color = "#00ff88"
        title_color = "#ffffff"
    else:
        bar_bg = "#f0f0f0"
        bar_border = "#cccccc"
        name_color = "#009944"
        title_color = "#222222"

    auth_state = st.session_state.get("auth_state")
    user = auth_state["user"] if auth_state else None
    display_name = get_display_name(user, role)

    st.markdown(
        f"""
        <div style="
            background:{bar_bg};
            border-bottom:1px solid {bar_border};
            padding:12px 16px;
            border-radius:6px;
        ">
            <span style="color:{name_color}; font-weight:600;">{display_name}</span>
            <h3 style="margin:4px 0 0 0; color:{title_color};">{title}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Logout", key=f"logout_{role}"):
        logout()


# ---------------------------------------------------------
# LOGOUT
# ---------------------------------------------------------
def logout() -> None:
    try:
        sb = get_supabase()
        sb.auth.sign_out()
    except Exception:
        pass

    st.session_state.clear()
    st.query_params.clear()
    st.rerun()
