import streamlit as st
from typing import Any, Dict


# -----------------------------
# THEME HELPERS
# -----------------------------
PRIMARY_BG = "#050608"
PRIMARY_CARD = "#111318"
ACCENT = "#00ff88"
ACCENT_SOFT = "rgba(0, 255, 136, 0.12)"
DANGER = "#e63946"
TEXT_MAIN = "#f5f5f5"
TEXT_MUTED = "#9ca3af"


def app_container_style():
    st.markdown(
        f"""
        <style>
        .main {{
            background: radial-gradient(circle at top left, #10141f 0, #050608 45%, #000000 100%);
            color: {TEXT_MAIN};
        }}
        .stButton>button {{
            background: linear-gradient(135deg, {ACCENT} 0%, #00c96b 100%);
            color: #000;
            border-radius: 999px;
            border: none;
            padding: 0.5rem 1.2rem;
            font-weight: 600;
        }}
        .stButton>button:hover {{
            filter: brightness(1.1);
        }}
        .neon-card {{
            background: {PRIMARY_CARD};
            border-radius: 16px;
            padding: 18px 20px;
            border: 1px solid {ACCENT_SOFT};
            box-shadow: 0 0 25px rgba(0, 255, 136, 0.08);
        }}
        .neon-pill {{
            display:inline-block;
            padding: 4px 10px;
            border-radius:999px;
            border:1px solid {ACCENT};
            color:{ACCENT};
            font-size:0.75rem;
            text-transform:uppercase;
            letter-spacing:0.08em;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def top_bar(title: str, role: str, logout_param: str):
    st.markdown(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            padding:12px 18px;
            background:linear-gradient(90deg,#020617,#020617,#0f172a);
            border-bottom:1px solid {ACCENT_SOFT};
            position:sticky;
            top:0;
            z-index:100;
        ">
            <div>
                <div class="neon-pill">{role}</div>
                <h3 style="margin:4px 0 0 0; color:{TEXT_MAIN};">
                    {title}
                </h3>
            </div>
            <a href='/?{logout_param}=true'
               style="
                    color:white;
                    background:{DANGER};
                    padding:8px 16px;
                    border-radius:999px;
                    text-decoration:none;
                    font-weight:600;
                    font-size:0.9rem;
               ">
                Logout
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------
# LOGOUT
# -----------------------------
def logout():
    st.session_state.clear()
    st.markdown(
        "<meta http-equiv='refresh' content='0; url=/' />",
        unsafe_allow_html=True
    )
    st.stop()

# def logout():
#     st.session_state.clear()
#     st.success("Logged out successfully.")
#     st.rerun()


# -----------------------------
# REQUIRE ADMIN / STUDENT
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
