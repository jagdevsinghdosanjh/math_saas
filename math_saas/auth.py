import streamlit as st
from typing import Any, Dict
from math_saas.utils.db import get_supabase
import re

# -----------------------------
# THEME COLORS
# -----------------------------
TEXT_MUTED = "#a0a6b1"
TEXT_MAIN = "#f8f9fa"
ACCENT = "#00ff88"
DANGER = "#ff4d6d"


# -----------------------------
# UNIVERSAL CONTAINER STYLE
# -----------------------------
def app_container_style():
    """Applies base container styling."""
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

    # ✅ Minimal valid iframe height
    st.iframe(
        src="https://cdn.jsdelivr.net/gh/jsd1973/mathjax-loader@main/mathjax.html",
        height=1,  # must be ≥1
    )


# -----------------------------
# PUBLIC CONTENT RENDERER
# -----------------------------

def render_public_content():
    """Render public content with proper LaTeX formatting."""
    sb = get_supabase()
    res = sb.table("public_content").select("*").order("created_at", desc=True).execute()
    items = [i for i in (res.data or []) if isinstance(i, dict)]

    for item in items:
        title = str(item.get("title", "Untitled"))
        body = str(item.get("body", ""))
        is_premium = bool(item.get("is_premium", False))

        st.markdown(f"### {title}")

        # ✅ Remove stray backslashes before $$ and normalize math blocks
        body = re.sub(r"\\\s*\$\$", "$$", body)
        body = re.sub(r"\$\$\s*\\", "$$", body)
        body = re.sub(r"\\\$", "$", body)

        # ✅ Split into math and non‑math segments
        parts = re.split(r"(\$\$.*?\$\$|\$.*?\$)", body)

        for part in parts:
            if re.match(r"(\$\$.*?\$\$|\$.*?\$)", part):
                clean = re.sub(r"^\$\$|^\$|\$\$|\$", "", part)
                st.latex(clean.strip())
            else:
                st.markdown(part)

        st.markdown(f"**Premium:** {is_premium}")


# -----------------------------
# DARK THEME — Neon Edition
# -----------------------------
def apply_dark_theme():
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


# -----------------------------
# LIGHT THEME — Minimal Edition
# -----------------------------
def apply_light_theme():
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


# -----------------------------
# TOP BAR COMPONENT
# -----------------------------
def top_bar(title: str, role: str, logout_param: str):
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


# -----------------------------
# LOGOUT HANDLER
# -----------------------------
def logout():
    st.session_state.clear()
    st.markdown("<meta http-equiv='refresh' content='0; url=/' />", unsafe_allow_html=True)
    st.stop()


# -----------------------------
# ROLE VALIDATION HELPERS
# -----------------------------
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
# from typing import Any, Dict
# from math_saas.utils.db import get_supabase
# import re

# # -----------------------------
# # THEME COLORS
# # -----------------------------
# TEXT_MUTED = "#a0a6b1"
# TEXT_MAIN = "#f8f9fa"
# ACCENT = "#00ff88"
# DANGER = "#ff4d6d"

# # -----------------------------
# # UNIVERSAL CONTAINER STYLE
# # -----------------------------
# def app_container_style():
#     """Applies base container styling."""
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


# # -----------------------------
# # PUBLIC CONTENT RENDERER
# # -----------------------------
# def render_public_content():
#     """Render public content with Streamlit-native LaTeX support."""
#     sb = get_supabase()

#     try:
#         res = sb.table("public_content").select("*").order("created_at", desc=True).execute()
#         items = [i for i in (res.data or []) if isinstance(i, dict)]
#     except Exception as e:
#         st.error(f"Error fetching content: {e}")
#         return

#     if not items:
#         st.info("No public content available.")
#         return

#     for item in items:
#         title = str(item.get("title", "Untitled"))
#         body_raw = item.get("body", "")
#         body = str(body_raw)  # ✅ ensure it's a string
#         is_premium = bool(item.get("is_premium", False))

#         st.markdown(f"### {title}")

#         # ✅ Split text into math and non‑math segments
#         parts = re.split(r"(\$\$.*?\$\$|\$.*?\$|\\\[.*?\\\]|\\\(.*?\\\))", body)

#         for part in parts:
#             if re.match(r"(\$\$.*?\$\$|\$.*?\$|\\\[.*?\\\]|\\\(.*?\\\))", part):
#                 clean = re.sub(r"^\$\$|^\$|\\\[|\\\(|\$\$|\\\]|\$|\\\)", "", part)
#                 st.latex(clean.strip())
#             else:
#                 st.markdown(part)

#         st.markdown(f"**Premium:** {is_premium}")


# # -----------------------------
# # DARK THEME — Neon Edition
# # -----------------------------
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


# # -----------------------------
# # LIGHT THEME — Minimal Edition
# # -----------------------------
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


# # -----------------------------
# # TOP BAR COMPONENT
# # -----------------------------
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


# # -----------------------------
# # LOGOUT HANDLER
# # -----------------------------
# def logout():
#     st.session_state.clear()
#     st.markdown("<meta http-equiv='refresh' content='0; url=/' />", unsafe_allow_html=True)
#     st.stop()


# # -----------------------------
# # ROLE VALIDATION HELPERS
# # -----------------------------
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