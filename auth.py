# import streamlit as st
# import re
# from typing import Any, Dict, List
# from utils.db import get_supabase

# TEXT_MUTED = "#a0a6b1"
# TEXT_MAIN = "#f8f9fa"
# ACCENT = "#00ff88"


# # ------------------------------------------------------------
# # GLOBAL STYLE
# # ------------------------------------------------------------
# def app_container_style() -> None:
#     st.markdown(
#         """<style>
#         body {
#             background: radial-gradient(circle at 20% 20%, #0f1115, #050608 60%);
#             color: #f8f9fa;
#             font-family: 'Inter', sans-serif;
#         }
#         .neon-card {
#             background: rgba(18, 20, 23, 0.65);
#             backdrop-filter: blur(12px);
#             border-radius: 14px;
#             padding: 20px;
#             border: 1px solid rgba(0,255,136,0.25);
#             box-shadow: 0 0 22px rgba(0,255,136,0.18);
#         }
#         h1, h2, h3, h4 {
#             color: #00ff88;
#             font-weight: 600;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )


# # ------------------------------------------------------------
# # SANITIZERS
# # ------------------------------------------------------------
# def sanitize_html(text: str) -> str:
#     if not isinstance(text, str):
#         return ""
#     text = re.sub(r"</?div[^>]*>", "", text, flags=re.IGNORECASE)
#     return text.replace("&nbsp;", " ").strip()


# def clean_math(text: Any) -> str:
#     if not isinstance(text, str):
#         return ""
#     text = text.replace("\\\\(", "\\(").replace("\\\\)", "\\)")
#     text = text.replace("\\\\[", "\\[").replace("\\\\]", "\\]")
#     text = text.replace("\\\\frac", "\\frac")
#     return re.sub(r"\$\s*\$", "$$", text)


# # ------------------------------------------------------------
# # PUBLIC CONTENT
# # ------------------------------------------------------------
# def render_public_content() -> None:
#     sb = get_supabase()
#     res = (
#         sb.table("public_content")
#         .select("*")
#         .order("created_at", desc=True)
#         .execute()
#     )
#     raw_items = getattr(res, "data", []) or []
#     items: List[Dict[str, Any]] = [
#         row for row in raw_items if isinstance(row, dict)
#     ]

#     if not items:
#         st.info("No public content available.")
#         return

#     for item in items:
#         title = str(item.get("title", "Untitled"))
#         body_raw = item.get("body", "")
#         body = sanitize_html(clean_math(body_raw))
#         st.markdown(f"### {title}")
#         st.markdown(body, unsafe_allow_html=True)


# # ------------------------------------------------------------
# # THEMES
# # ------------------------------------------------------------
# def apply_dark_theme() -> None:
#     st.markdown(
#         "<style>.main { background: #050608; color: #f8f9fa; }</style>",
#         unsafe_allow_html=True,
#     )


# def apply_light_theme() -> None:
#     st.markdown(
#         "<style>.main { background: #ffffff; color: #111827; }</style>",
#         unsafe_allow_html=True,
#     )


# # ------------------------------------------------------------
# # TOP BAR
# # ------------------------------------------------------------
# def top_bar(title: str, role: str, logout_param: str) -> None:
#     auth_state = st.session_state.get("auth_state", {})
#     user = auth_state.get("user", {})

#     display_name = (
#         user.get("full_name")
#         or user.get("name")
#         or user.get("email")
#         or role.capitalize()
#     )

#     st.markdown(
#         f"""
#         <div style="background:#0a0c10; border-bottom:1px solid #00ff88; padding:12px 16px;">
#             <span style="color:#00ff88; font-weight:600;">{display_name}</span>
#             <h3 style="margin:4px 0 0 0; color:white;">{title}</h3>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     if st.button("Logout", key=f"logout_{role}"):
#         logout()


# # ------------------------------------------------------------
# # AUTH STATE (NEW MODEL)
# # ------------------------------------------------------------
# def set_logged_in_user(profile, role, session):
#     """
#     Store unified auth state:
#     - profile (from profiles table)
#     - role (admin/student)
#     - access_token
#     - refresh_token
#     - session_user_id (auth.uid())
#     """

#     st.session_state["auth_state"] = {
#         "user": profile,
#         "role": role,
#         "access_token": session.access_token,
#         "refresh_token": session.refresh_token,
#         "session_user_id": session.user.id,  # CRITICAL FOR RLS
#     }

#     # Remove deprecated keys
#     for key in ["user", "role", "jwt", "student", "admin"]:
#         st.session_state.pop(key, None)


# def restore_session() -> None:
#     """Restore Supabase session + app auth state."""
#     auth_state = st.session_state.get("auth_state")
#     if not auth_state:
#         return

#     access_token = auth_state.get("access_token")
#     refresh_token = auth_state.get("refresh_token")

#     if access_token and refresh_token:
#         sb = get_supabase()
#         sb.auth.set_session(access_token, refresh_token)


# # ------------------------------------------------------------
# # LOGOUT
# # ------------------------------------------------------------
# def logout() -> None:
#     try:
#         sb = get_supabase()
#         sb.auth.sign_out()
#     except Exception:
#         pass

#     for key in ["auth_state", "login_mode", "session"]:
#         st.session_state.pop(key, None)

#     st.query_params.clear()
#     st.rerun()


# # ------------------------------------------------------------
# # ROLE HELPERS
# # ------------------------------------------------------------
# def require_admin() -> None:
#     auth_state = st.session_state.get("auth_state", {})
#     if auth_state.get("role") != "admin":
#         st.error("Please login as admin.")
#         st.stop()


# def require_student() -> None:
#     auth_state = st.session_state.get("auth_state", {})
#     if auth_state.get("role") != "student":
#         st.error("Please login as student.")
#         st.stop()

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
# THEMES
# ------------------------------------------------------------
def apply_dark_theme() -> None:
    st.markdown(
        "<style>.main { background: #050608; color: #f8f9fa; }</style>",
        unsafe_allow_html=True,
    )

def apply_light_theme() -> None:
    st.markdown(
        "<style>.main { background: #ffffff; color: #111827; }</style>",
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------
# TOP BAR
# ------------------------------------------------------------
def top_bar(title: str, role: str, logout_param: str) -> None:
    user = st.session_state.get("user", {})
    display_name = (
        user.get("full_name")
        or user.get("name")
        or user.get("email")
        or role.capitalize()
    )
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
# AUTH PERSISTENCE (SINGLE MODEL)
# # ------------------------------------------------------------
def set_logged_in_user(profile, role, access_token, refresh_token):
    # Store user and tokens
    st.session_state["user"] = profile
    st.session_state["role"] = role
    st.session_state["access_token"] = access_token
    st.session_state["refresh_token"] = refresh_token

    # Preserve Supabase session if it exists
    supabase_session = st.session_state.get("session")

    # Remove old auth keys (cleanup)
    for key in ["jwt", "student", "admin", "auth_state"]:
        st.session_state.pop(key, None)

    # Restore Supabase session
    if supabase_session is not None:
        st.session_state["session"] = supabase_session

def restore_session() -> None:
    """Restore Supabase + logical auth from auth_state, if present."""
    # Ensure keys exist
    st.session_state.setdefault("user", None)
    st.session_state.setdefault("role", None)
    st.session_state.setdefault("jwt", None)

    session = st.session_state.get("session")
    auth_state = st.session_state.get("auth_state")

    # Restore Supabase session
    if session:
        sb = get_supabase()
        access_token = getattr(session, "access_token", None)
        refresh_token = getattr(session, "refresh_token", None)
        if access_token and refresh_token:
            sb.auth.set_session(access_token, refresh_token)

    # Restore app login state
    if auth_state:
        st.session_state["user"] = auth_state.get("user")
        st.session_state["role"] = auth_state.get("role")
        st.session_state["jwt"] = auth_state.get("jwt")

# ------------------------------------------------------------
# LOGOUT
# ------------------------------------------------------------
def logout() -> None:
    # Optional: sign out from Supabase too
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
