import streamlit as st
from typing import Any, Dict

# -----------------------------
# THEME COLORS
# -----------------------------
TEXT_MUTED = "#a0a6b1"  # ✅ ensure this exists for other modules
TEXT_MAIN = "#f8f9fa"
ACCENT = "#00ff88"
DANGER = "#ff4d6d"


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
            transition: background 0.5s ease;
        }
        .stButton>button {
            background: linear-gradient(135deg, #00ff88 0%, #00c96b 100%);
            color: #000;
            border-radius: 999px;
            border: none;
            padding: 0.6rem 1.4rem;
            font-weight: 600;
            box-shadow: 0 0 12px rgba(0, 255, 136, 0.3);
            transition: all 0.25s ease;
        }
        .stButton>button:hover {
            filter: brightness(1.15);
            transform: translateY(-1px);
        }
        .neon-card {
            background: #121417;
            border-radius: 14px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 0 18px rgba(0,255,136,0.25);
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
            transition: background 0.5s ease;
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
        .neon-card {
            background: #ffffff;
            border-radius: 14px;
            padding: 20px;
            border: 1px solid rgba(0,0,0,0.08);
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
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
#             transition: background 0.5s ease;
#         }
#         .stButton>button {
#             background: linear-gradient(135deg, #00ff88 0%, #00c96b 100%);
#             color: #000;
#             border-radius: 999px;
#             border: none;
#             padding: 0.6rem 1.4rem;
#             font-weight: 600;
#             box-shadow: 0 0 12px rgba(0, 255, 136, 0.3);
#             transition: all 0.25s ease;
#         }
#         .stButton>button:hover {
#             filter: brightness(1.15);
#             transform: translateY(-1px);
#         }
#         .neon-card {
#             background: #121417;
#             border-radius: 14px;
#             padding: 20px;
#             border: 1px solid rgba(255,255,255,0.08);
#             box-shadow: 0 0 18px rgba(0,255,136,0.25);
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
#             transition: background 0.5s ease;
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
#         .neon-card {
#             background: #ffffff;
#             border-radius: 14px;
#             padding: 20px;
#             border: 1px solid rgba(0,0,0,0.08);
#             box-shadow: 0 2px 10px rgba(0,0,0,0.05);
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


# import streamlit as st
# from typing import Any, Dict

# # -----------------------------
# # THEME PALETTE — Refined Neon Edition
# # -----------------------------
# PRIMARY_BG = "linear-gradient(135deg, #050608 0%, #0a0c10 100%)"
# PRIMARY_CARD = "#121417"
# ACCENT = "#00ff88"
# ACCENT_SOFT = "rgba(0, 255, 136, 0.15)"
# DANGER = "#ff4d6d"
# TEXT_MAIN = "#f8f9fa"
# TEXT_MUTED = "#a0a6b1"
# BORDER_COLOR = "rgba(255, 255, 255, 0.08)"
# SHADOW = "0 0 18px rgba(0, 255, 136, 0.25)"


# # -----------------------------
# # GLOBAL CONTAINER STYLE
# # -----------------------------
# def app_container_style():
#     st.markdown(
#         f"""
#         <style>
#         /* Background and typography */
#         .main {{
#             background: {PRIMARY_BG};
#             color: {TEXT_MAIN};
#             font-family: 'Inter', 'Segoe UI', sans-serif;
#         }}

#         /* Buttons */
#         .stButton>button {{
#             background: linear-gradient(135deg, {ACCENT} 0%, #00c96b 100%);
#             color: #000;
#             border-radius: 999px;
#             border: none;
#             padding: 0.6rem 1.4rem;
#             font-weight: 600;
#             letter-spacing: 0.03em;
#             box-shadow: 0 0 12px rgba(0, 255, 136, 0.3);
#             transition: all 0.25s ease;
#         }}
#         .stButton>button:hover {{
#             filter: brightness(1.15);
#             transform: translateY(-1px);
#         }}

#         /* Card styling */
#         .neon-card {{
#             background: {PRIMARY_CARD};
#             border-radius: 14px;
#             padding: 20px 22px;
#             border: 1px solid {BORDER_COLOR};
#             box-shadow: {SHADOW};
#             transition: all 0.3s ease;
#         }}
#         .neon-card:hover {{
#             border-color: {ACCENT};
#             box-shadow: 0 0 25px {ACCENT_SOFT};
#         }}

#         /* Pill badges */
#         .neon-pill {{
#             display:inline-block;
#             padding: 5px 12px;
#             border-radius:999px;
#             border:1px solid {ACCENT};
#             color:{ACCENT};
#             font-size:0.75rem;
#             text-transform:uppercase;
#             letter-spacing:0.08em;
#             background:rgba(0,255,136,0.05);
#         }}

#         /* Headings and text */
#         h3, h4 {{
#             color:{ACCENT};
#             font-weight:600;
#             margin-bottom:6px;
#         }}
#         p {{
#             color:{TEXT_MUTED};
#             line-height:1.6;
#         }}
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
#             border-bottom:1px solid {ACCENT_SOFT};
#             position:sticky;
#             top:0;
#             z-index:100;
#             box-shadow:0 2px 8px rgba(0,0,0,0.4);
#         ">
#             <div>
#                 <div class="neon-pill">{role}</div>
#                 <h3 style="margin:4px 0 0 0; color:{TEXT_MAIN};">
#                     {title}
#                 </h3>
#             </div>
#             <a href='/?{logout_param}=true'
#                style="
#                     color:white;
#                     background:{DANGER};
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

# # import streamlit as st
# # from typing import Any, Dict


# # # -----------------------------
# # # THEME HELPERS
# # # -----------------------------
# # PRIMARY_BG = "#050608"
# # PRIMARY_CARD = "#111318"
# # ACCENT = "#00ff88"
# # ACCENT_SOFT = "rgba(0, 255, 136, 0.12)"
# # DANGER = "#e63946"
# # TEXT_MAIN = "#f5f5f5"
# # TEXT_MUTED = "#9ca3af"


# # def app_container_style():
# #     st.markdown(
# #         f"""
# #         <style>
# #         .main {{
# #             background: radial-gradient(circle at top left, #10141f 0, #050608 45%, #000000 100%);
# #             color: {TEXT_MAIN};
# #         }}
# #         .stButton>button {{
# #             background: linear-gradient(135deg, {ACCENT} 0%, #00c96b 100%);
# #             color: #000;
# #             border-radius: 999px;
# #             border: none;
# #             padding: 0.5rem 1.2rem;
# #             font-weight: 600;
# #         }}
# #         .stButton>button:hover {{
# #             filter: brightness(1.1);
# #         }}
# #         .neon-card {{
# #             background: {PRIMARY_CARD};
# #             border-radius: 16px;
# #             padding: 18px 20px;
# #             border: 1px solid {ACCENT_SOFT};
# #             box-shadow: 0 0 25px rgba(0, 255, 136, 0.08);
# #         }}
# #         .neon-pill {{
# #             display:inline-block;
# #             padding: 4px 10px;
# #             border-radius:999px;
# #             border:1px solid {ACCENT};
# #             color:{ACCENT};
# #             font-size:0.75rem;
# #             text-transform:uppercase;
# #             letter-spacing:0.08em;
# #         }}
# #         </style>
# #         """,
# #         unsafe_allow_html=True,
# #     )


# # def top_bar(title: str, role: str, logout_param: str):
# #     st.markdown(
# #         f"""
# #         <div style="
# #             display:flex;
# #             justify-content:space-between;
# #             align-items:center;
# #             padding:12px 18px;
# #             background:linear-gradient(90deg,#020617,#020617,#0f172a);
# #             border-bottom:1px solid {ACCENT_SOFT};
# #             position:sticky;
# #             top:0;
# #             z-index:100;
# #         ">
# #             <div>
# #                 <div class="neon-pill">{role}</div>
# #                 <h3 style="margin:4px 0 0 0; color:{TEXT_MAIN};">
# #                     {title}
# #                 </h3>
# #             </div>
# #             <a href='/?{logout_param}=true'
# #                style="
# #                     color:white;
# #                     background:{DANGER};
# #                     padding:8px 16px;
# #                     border-radius:999px;
# #                     text-decoration:none;
# #                     font-weight:600;
# #                     font-size:0.9rem;
# #                ">
# #                 Logout
# #             </a>
# #         </div>
# #         """,
# #         unsafe_allow_html=True,
# #     )


# # # -----------------------------
# # # LOGOUT
# # # -----------------------------
# # def logout():
# #     st.session_state.clear()
# #     st.markdown(
# #         "<meta http-equiv='refresh' content='0; url=/' />",
# #         unsafe_allow_html=True
# #     )
# #     st.stop()

# # # def logout():
# # #     st.session_state.clear()
# # #     st.success("Logged out successfully.")
# # #     st.rerun()


# # # -----------------------------
# # # REQUIRE ADMIN / STUDENT
# # # -----------------------------
# # def require_admin() -> Dict[str, Any]:
# #     admin = st.session_state.get("admin")
# #     if not admin:
# #         st.error("Please login as admin.")
# #         st.stop()
# #     return admin


# # def require_student() -> Dict[str, Any]:
# #     student = st.session_state.get("student")
# #     if not student:
# #         st.error("Please login as student.")
# #         st.stop()
# #     return student
