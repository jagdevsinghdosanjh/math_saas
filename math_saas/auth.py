import streamlit as st
import re
from typing import Any, Dict, List, cast
from math_saas.utils.db import get_supabase

TEXT_MUTED = "#a0a6b1"
TEXT_MAIN = "#f8f9fa"
ACCENT = "#00ff88"   # neon green accent used across UI

# ------------------------------------------------------------
# GLOBAL STYLE
# # ------------------------------------------------------------
def app_container_style() -> None:
    st.markdown(
        """
        <style>

        /* ------------------------------
           GLOBAL BACKGROUND
        ------------------------------ */
        body {
            background: radial-gradient(circle at 20% 20%, #0f1115, #050608 60%);
            color: #f8f9fa;
            font-family: 'Inter', sans-serif;
            transition: background 0.4s ease-in-out;
        }

        /* ------------------------------
           GLASS EFFECT CARDS
        ------------------------------ */
        .neon-card {
            background: rgba(18, 20, 23, 0.65);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 14px;
            padding: 20px;
            border: 1px solid rgba(0,255,136,0.25);
            box-shadow: 0 0 22px rgba(0,255,136,0.18);
            transition: transform 0.25s ease, box-shadow 0.25s ease;
        }

        .neon-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 0 28px rgba(0,255,136,0.35);
        }

        /* ------------------------------
           HEADINGS
        ------------------------------ */
        h1, h2, h3, h4 {
            color: #00ff88;
            letter-spacing: 0.5px;
            font-weight: 600;
        }

        /* ------------------------------
           PARAGRAPHS
        ------------------------------ */
        p {
            color: #b5b8c2;
            line-height: 1.6;
        }

        /* ------------------------------
           STREAMLIT WIDGETS
        ------------------------------ */
        .stButton>button {
            background: linear-gradient(135deg, #00ff88, #00cc6a);
            color: black;
            border-radius: 8px;
            padding: 8px 18px;
            border: none;
            font-weight: 600;
            transition: 0.25s ease;
        }

        .stButton>button:hover {
            background: linear-gradient(135deg, #00ffaa, #00dd77);
            transform: translateY(-2px);
            box-shadow: 0 0 12px rgba(0,255,136,0.45);
        }

        /* ------------------------------
           TABS
        ------------------------------ */
        .stTabs [data-baseweb="tab"] {
            background: #0d0f12;
            border-radius: 8px;
            padding: 10px 16px;
            margin-right: 6px;
            color: #9ca3af;
            border: 1px solid rgba(255,255,255,0.08);
        }

        .stTabs [aria-selected="true"] {
            background: #00ff88 !important;
            color: black !important;
            font-weight: 600;
            border: 1px solid #00ff88;
        }

        /* ------------------------------
           SCROLLBAR
        ------------------------------ */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-thumb {
            background: #00ff88;
            border-radius: 10px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

# def app_container_style() -> None:
#     st.markdown(
#         """
#         <style>
#         body {
#             background: linear-gradient(135deg, #050608 0%, #0a0c10 100%);
#             color: #00FFFF;
#             font-family: 'Inter', sans-serif;
#         }
#         .neon-card {
#             background: #00FFFF;
#             border-radius: 14px;
#             padding: 20px;
#             border: 1px solid rgba(55,55,55,0.08);
#             box-shadow: 0 0 18px rgba(0,255,136,0.25);
#         }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

def sanitize_html(text: str) -> str:
    if not isinstance(text, str):
        return ""

    # Remove all <div> and </div> tags
    text = re.sub(r"</?div[^>]*>", "", text, flags=re.IGNORECASE)

    # Remove empty HTML artifacts
    text = text.replace("&nbsp;", " ").strip()

    return text

# ------------------------------------------------------------
# CLEAN MATH
# ------------------------------------------------------------
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
        body_raw = item.get("body", "")
        body = sanitize_html(clean_math(body_raw))
        st.markdown(body, unsafe_allow_html=True)

        # body_raw: Any = item.get("body", "")
        # body: str = sanitize_html(clean_math(body_raw))
        # # body: str = clean_math(body_raw)

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
    """
    Streamlit-native top bar with personalized name display.
    """

    # Determine displayed name
    user = st.session_state.get(role, {})
    display_name = user.get("full_name") or user.get("name") or role.capitalize()

    st.markdown(
        f"""
        <div style="
            background:#0a0c10;
            border-bottom:1px solid #00ff88;
            padding:12px 16px;
        ">
            <span style="color:#00ff88; font-weight:600; font-size:0.9rem;">
                {display_name}
            </span>
            <h3 style="margin:4px 0 0 0; color:white;">{title}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([6, 1])

    with col2:
        if st.button("Logout", key=f"logout_{role}", use_container_width=True):
            st.query_params[logout_param] = "true"
            st.rerun()
# ------------------------------------------------------------
# AUTH PERSISTENCE
# ------------------------------------------------------------
def set_logged_in_user(user: Dict[str, Any], role: str, jwt: str) -> None:
    st.session_state[role] = user
    st.session_state["jwt"] = jwt

    st.query_params = {"token": jwt, "role": role}


def restore_session() -> None:
    params = dict(st.query_params)

    # Prevent auto-login after logout
    if params.get("student_logout") == "true" or params.get("admin_logout") == "true":
        return

    token = params.get("token")
    role = params.get("role")

    if not token or not role:
        return

    # Already logged in
    if "student" in st.session_state or "admin" in st.session_state:
        return

    sb = get_supabase()
    try:
        user_resp = sb.auth.get_user(token)
    except Exception:
        return

    user = getattr(user_resp, "user", None)
    if not user:
        return

    st.session_state["jwt"] = token
    st.session_state[role] = user

# ------------------------------------------------------------
# LOGOUT (FINAL FIXED VERSION)
# ------------------------------------------------------------
def logout() -> None:
    """
    Clears ONLY authentication-related session keys,
    clears URL params, and forces a clean rerun.
    """

    # 1. Remove only auth keys (never clear all keys)
    for key in ["student", "admin", "role", "jwt", "authenticated", "login_mode"]:
        if key in st.session_state:
            del st.session_state[key]

    # 2. Clear ALL query params (critical)
    st.query_params.clear()

    # 3. Force a clean rerun
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
