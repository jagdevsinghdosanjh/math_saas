import re
from typing import Any, Dict

import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

from math_saas.utils.db import get_supabase


# ============================================================
#  THEME COLORS
# ============================================================
TEXT_MUTED = "#a0a6b1"
TEXT_MAIN = "#f8f9fa"
ACCENT = "#00ff88"
DANGER = "#ff4d6d"


# ============================================================
#  COOKIE MANAGER (PERSISTENT AUTH)
# ============================================================
cookies = EncryptedCookieManager(
    prefix="math_saas_",
    password="CHANGE_THIS_TO_A_STRONG_SECRET",
)


def _cookies_ready() -> bool:
    # Avoid crashes if cookies not initialized yet
    try:
        return cookies.ready()
    except Exception:
        return False


# ============================================================
#  GLOBAL STYLE + KATEX
# ============================================================
def app_container_style() -> None:
    """Inject global CSS + KaTeX loader."""
    st.markdown(
        f"""
        <style>
        body {{
            background: linear-gradient(135deg, #050608 0%, #0a0c10 100%);
            color: {TEXT_MAIN};
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }}
        .neon-card {{
            background: #121417;
            border-radius: 14px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 0 18px rgba(0,255,136,0.25);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <link rel="stylesheet"
              href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">

        <script defer
                src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js">
        </script>

        <script defer
                src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
                onload="renderMathInElement(document.body, {
                    delimiters: [
                        {left: '$$', right: '$$', display: true},
                        {left: '$', right: '$', display: false},
                        {left: '\\\\(', right: '\\\\)', display: false}
                    ]
                });">
        </script>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
#  MATH CLEANING
# ============================================================
def clean_math(text: str) -> str:
    if not text:
        return ""

    text = text.replace("\\\\(", "\\(")
    text = text.replace("\\\\)", "\\)")
    text = text.replace("\\\\[", "\\[")
    text = text.replace("\\\\]", "\\]")
    text = text.replace("\\\\frac", "\\frac")
    text = re.sub(r"\$\s*\$", "$$", text)

    return text


# ============================================================
#  PUBLIC CONTENT
# ============================================================
def render_public_content() -> None:
    sb = get_supabase()
    res = (
        sb.table("public_content")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    items = [i for i in (res.data or []) if isinstance(i, dict)]

    for item in items:
        title = str(item.get("title", "Untitled"))
        body = clean_math(str(item.get("body", "")))
        is_premium = bool(item.get("is_premium", False))

        st.markdown(f"### {title}")
        st.markdown(body, unsafe_allow_html=True)

        st.markdown(
            """
            <script>
                renderMathInElement(document.body, {
                    delimiters: [
                        {left: '$$', right: '$$', display: true},
                        {left: '$', right: '$', display: false},
                        {left: '\\\\(', right: '\\\\)', display: false}
                    ]
                });
            </script>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(f"**Premium:** {is_premium}")


# ============================================================
#  THEMES
# ============================================================
def apply_dark_theme() -> None:
    st.markdown(
        """
        <style>
        .main {
            background: linear-gradient(135deg, #050608 0%, #0a0c10 100%);
            color: #f8f9fa;
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }
        .stButton>button {
            background: linear-gradient(135deg, #00ff88 0%, #00c96b 100%);
            color: #000;
            border-radius: 999px;
            border: none;
            padding: 0.6rem 1.4rem;
            font-weight: 600;
            box-shadow: 0 0 12px rgba(0,255,136,0.3);
            transition: all 0.25s ease;
        }
        .stButton>button:hover {
            filter: brightness(1.15);
            transform: translateY(-1px);
        }
        h3, h4 { color: #00ff88; font-weight: 600; }
        p { color: #a0a6b1; line-height: 1.6; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def apply_light_theme() -> None:
    st.markdown(
        """
        <style>
        .main {
            background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
            color: #111827;
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }
        .stButton>button {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            border-radius: 999px;
            border: none;
            padding: 0.6rem 1.4rem;
            font-weight: 600;
            box-shadow: 0 0 10px rgba(16,185,129,0.25);
            transition: all 0.25s ease;
        }
        .stButton>button:hover {
            filter: brightness(1.15);
            transform: translateY(-1px);
        }
        h3, h4 { color: #059669; font-weight: 600; }
        p { color: #374151; line-height: 1.6; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
#  TOP BAR
# ============================================================
def top_bar(title: str, role: str, logout_param: str) -> None:
    st.markdown(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            padding:12px 18px;
            background:linear-gradient(90deg,#020617,#0a0c10,#0f172a);
            border-bottom:1px solid rgba(0,255,136,0.15);
            position:sticky;
            top:0;
            z-index:100;
            box-shadow:0 2px 8px rgba(0,0,0,0.4);
        ">
            <div>
                <div style='
                    display:inline-block;
                    padding:5px 12px;
                    border-radius:999px;
                    border:1px solid #00ff88;
                    color:#00ff88;
                    font-size:0.75rem;
                    text-transform:uppercase;
                    letter-spacing:0.08em;
                    background:rgba(0,255,136,0.05);
                '>{role}</div>
                <h3 style="margin:4px 0 0 0; color:#f8f9fa;">{title}</h3>
            </div>
            <a href='/?{logout_param}=true'
               style="
                    color:white;
                    background:#ff4d6d;
                    padding:8px 16px;
                    border-radius:999px;
                    text-decoration:none;
                    font-weight:600;
                    font-size:0.9rem;
                    box-shadow:0 0 10px rgba(255,77,109,0.4);
                    transition:all 0.25s ease;
               "
               onmouseover="this.style.filter='brightness(1.15)'"
               onmouseout="this.style.filter='brightness(1)'">
                Logout
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
#  AUTH PERSISTENCE
# ============================================================
def set_logged_in_user(user: Dict[str, Any], role: str, jwt: str) -> None:
    """
    Call this AFTER successful Supabase login.

    user: Supabase user dict
    role: "student" or "admin"
    jwt:  access token from Supabase session
    """
    st.session_state[role] = user
    st.session_state["jwt"] = jwt

    if _cookies_ready():
        cookies["jwt"] = jwt
        cookies["role"] = role
        cookies.save()


def restore_session() -> None:
    """
    Call this at the top of your main app script.
    Restores logged-in user from cookies if session_state is empty.
    """
    if not _cookies_ready():
        return

    if "student" in st.session_state or "admin" in st.session_state:
        return

    token = cookies.get("jwt")
    role = cookies.get("role")

    if not token or not role:
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
    if role == "student":
        st.session_state["student"] = user
    elif role == "admin":
        st.session_state["admin"] = user


def logout() -> None:
    if _cookies_ready():
        cookies["jwt"] = ""
        cookies["role"] = ""
        cookies.save()

    st.session_state.clear()
    st.markdown("<meta http-equiv='refresh' content='0; url=/' />", unsafe_allow_html=True)
    st.stop()


# ============================================================
#  ROLE HELPERS
# ============================================================
def require_admin() -> Dict[str, Any]:
    admin = st.session_state.get("admin")
    if not admin:
        st.error("Please login as admin.")
        st.stop()
    return admin


def require_student() -> Dict[str, Any]:
    student = st.session_state.get("student")
    if not student:
        st.error("Please login as student.")
        st.stop()
    return student

# import streamlit as st
# import re
# from typing import Any, Dict
# from math_saas.utils.db import get_supabase


# # ============================================================
# #  THEME COLORS
# # ============================================================
# TEXT_MUTED = "#a0a6b1"
# TEXT_MAIN = "#f8f9fa"
# ACCENT = "#00ff88"
# DANGER = "#ff4d6d"


# # ============================================================
# #  KATEX + GLOBAL STYLE LOADER
# # ============================================================
# def app_container_style():
#     """Inject global CSS + KaTeX loader."""
#     st.markdown(
#         f"""
#         <style>
#         body {{
#             background: linear-gradient(135deg, #050608 0%, #0a0c10 100%);
#             color: {TEXT_MAIN};
#             font-family: 'Inter', 'Segoe UI', sans-serif;
#         }}
#         .neon-card {{
#             background: #121417;
#             border-radius: 14px;
#             padding: 20px;
#             border: 1px solid rgba(255,255,255,0.08);
#             box-shadow: 0 0 18px rgba(0,255,136,0.25);
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

#     # Correct KaTeX loader
#     st.markdown(
#         """
#         <link rel="stylesheet"
#               href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">

#         <script defer
#                 src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js">
#         </script>

#         <script defer
#                 src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
#                 onload="renderMathInElement(document.body, {
#                     delimiters: [
#                         {left: '$$', right: '$$', display: true},
#                         {left: '$', right: '$', display: false},
#                         {left: '\\\\(', right: '\\\\)', display: false}
#                     ]
#                 });">
#         </script>
#         """,
#         unsafe_allow_html=True,
#     )


# # ============================================================
# #  MATH CLEANING UTILITY
# # ============================================================
# def clean_math(text: str) -> str:
#     """Fix escaped LaTeX from Supabase."""
#     if not text:
#         return ""

#     text = text.replace("\\\\(", "\\(")
#     text = text.replace("\\\\)", "\\)")
#     text = text.replace("\\\\[", "\\[")
#     text = text.replace("\\\\]", "\\]")
#     text = text.replace("\\\\frac", "\\frac")
#     text = re.sub(r"\$\s*\$", "$$", text)

#     return text


# # ============================================================
# #  PUBLIC CONTENT RENDERER
# # ============================================================
# def render_public_content():
#     """Render public content with KaTeX-enabled Markdown."""
#     sb = get_supabase()
#     res = sb.table("public_content").select("*").order("created_at", desc=True).execute()
#     items = [i for i in (res.data or []) if isinstance(i, dict)]

#     for item in items:
#         title = str(item.get("title", "Untitled"))
#         body = clean_math(str(item.get("body", "")))
#         is_premium = bool(item.get("is_premium", False))

#         st.markdown(f"### {title}")
#         st.markdown(body, unsafe_allow_html=True)

#         # Re-trigger KaTeX for this block
#         st.markdown(
#             """
#             <script>
#                 renderMathInElement(document.body, {
#                     delimiters: [
#                         {left: '$$', right: '$$', display: true},
#                         {left: '$', right: '$', display: false},
#                         {left: '\\\\(', right: '\\\\)', display: false}
#                     ]
#                 });
#             </script>
#             """,
#             unsafe_allow_html=True,
#         )

#         st.markdown(f"**Premium:** {is_premium}")


# # ============================================================
# #  DARK THEME — Neon Edition
# # ============================================================
# def apply_dark_theme():
#     st.markdown(
#         """
#         <style>
#         .main {
#             background: linear-gradient(135deg, #050608 0%, #0a0c10 100%);
#             color: #f8f9fa;
#             font-family: 'Inter', 'Segoe UI', sans-serif;
#         }
#         .stButton>button {
#             background: linear-gradient(135deg, #00ff88 0%, #00c96b 100%);
#             color: #000;
#             border-radius: 999px;
#             border: none;
#             padding: 0.6rem 1.4rem;
#             font-weight: 600;
#             box-shadow: 0 0 12px rgba(0,255,136,0.3);
#             transition: all 0.25s ease;
#         }
#         .stButton>button:hover {
#             filter: brightness(1.15);
#             transform: translateY(-1px);
#         }
#         h3, h4 { color: #00ff88; font-weight: 600; }
#         p { color: #a0a6b1; line-height: 1.6; }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )


# # ============================================================
# #  LIGHT THEME — Minimal Edition
# # ============================================================
# def apply_light_theme():
#     st.markdown(
#         """
#         <style>
#         .main {
#             background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
#             color: #111827;
#             font-family: 'Inter', 'Segoe UI', sans-serif;
#         }
#         .stButton>button {
#             background: linear-gradient(135deg, #10b981 0%, #059669 100%);
#             color: white;
#             border-radius: 999px;
#             border: none;
#             padding: 0.6rem 1.4rem;
#             font-weight: 600;
#             box-shadow: 0 0 10px rgba(16,185,129,0.25);
#             transition: all 0.25s ease;
#         }
#         .stButton>button:hover {
#             filter: brightness(1.15);
#             transform: translateY(-1px);
#         }
#         h3, h4 { color: #059669; font-weight: 600; }
#         p { color: #374151; line-height: 1.6; }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )


# # ============================================================
# #  TOP BAR COMPONENT
# # ============================================================
# def top_bar(title: str, role: str, logout_param: str):
#     st.markdown(
#         f"""
#         <div style="
#             display:flex;
#             justify-content:space-between;
#             align-items:center;
#             padding:12px 18px;
#             background:linear-gradient(90deg,#020617,#0a0c10,#0f172a);
#             border-bottom:1px solid rgba(0,255,136,0.15);
#             position:sticky;
#             top:0;
#             z-index:100;
#             box-shadow:0 2px 8px rgba(0,0,0,0.4);
#         ">
#             <div>
#                 <div style='
#                     display:inline-block;
#                     padding:5px 12px;
#                     border-radius:999px;
#                     border:1px solid #00ff88;
#                     color:#00ff88;
#                     font-size:0.75rem;
#                     text-transform:uppercase;
#                     letter-spacing:0.08em;
#                     background:rgba(0,255,136,0.05);
#                 '>{role}</div>
#                 <h3 style="margin:4px 0 0 0; color:#f8f9fa;">{title}</h3>
#             </div>
#             <a href='/?{logout_param}=true'
#                style="
#                     color:white;
#                     background:#ff4d6d;
#                     padding:8px 16px;
#                     border-radius:999px;
#                     text-decoration:none;
#                     font-weight:600;
#                     font-size:0.9rem;
#                     box-shadow:0 0 10px rgba(255,77,109,0.4);
#                     transition:all 0.25s ease;
#                "
#                onmouseover="this.style.filter='brightness(1.15)'"
#                onmouseout="this.style.filter='brightness(1)'">
#                 Logout
#             </a>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )


# # ============================================================
# #  LOGOUT HANDLER
# # ============================================================
# def logout():
#     st.session_state.clear()
#     st.markdown("<meta http-equiv='refresh' content='0; url=/' />", unsafe_allow_html=True)
#     st.stop()


# # ============================================================
# #  ROLE VALIDATION HELPERS
# # ============================================================
# def require_admin() -> Dict[str, Any]:
#     admin = st.session_state.get("admin")
#     if not admin:
#         st.error("Please login as admin.")
#         st.stop()
#     return admin


# def require_student() -> Dict[str, Any]:
#     student = st.session_state.get("student")
#     if not student:
#         st.error("Please login as student.")
#         st.stop()
#     return student