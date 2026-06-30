import streamlit as st

def is_dark_theme():
    return st.session_state.get("theme_choice", "Dark (Neon)") == "Dark (Neon)"


# ============================================================
# DARK NEON THEME — Premium SaaS + Neon Accents
# ============================================================
def apply_dark_theme():
    st.markdown(
        """
        <style>

        body, .stApp {
            background: radial-gradient(circle at 20% 20%, #0f1115, #050608 60%) !important;
            color: #f8f9fa !important;
            font-family: 'Inter', sans-serif;
        }

        /* Universal text */
        p, span, label, h1, h2, h3, h4, h5, h6, div {
            color: #f8f9fa !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #0d0f12 !important;
        }

        /* Buttons */
        .stButton>button {
            background-color: #1a1d23 !important;
            color: #f8f9fa !important;
            border: 1px solid #333 !important;
            border-radius: 6px !important;
        }
        .stButton>button:hover {
            background-color: #23272f !important;
            border-color: #666 !important;
        }

        /* Inputs */
        input, textarea, select {
            background-color: #1a1d23 !important;
            color: #f8f9fa !important;
            border: 1px solid #333 !important;
        }

        /* Cards */
        .app-card {
            background: rgba(18, 20, 23, 0.65) !important;
            border-radius: 14px;
            padding: 20px;
            border: 1px solid rgba(0,255,136,0.25) !important;
            box-shadow: 0 0 22px rgba(0,255,136,0.18) !important;
        }

        /* Headings */
        h1, h2, h3, h4 {
            color: #00ff88 !important;
            font-weight: 600;
        }

        /* Status colors */
        .status-ok { color: #00ff88 !important; font-weight: bold; }
        .status-down { color: #ff4d4d !important; font-weight: bold; }
        .status-warn { color: #ffcc00 !important; font-weight: bold; }

        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# LIGHT THEME — Clean, Professional, High Readability
# ============================================================
def apply_light_theme():
    st.markdown(
        """
        <style>

        body, .stApp {
            background-color: #ffffff !important;
            color: #222222 !important;
            font-family: 'Inter', sans-serif;
        }

        p, span, label, h1, h2, h3, h4, h5, h6, div {
            color: #222222 !important;
        }

        section[data-testid="stSidebar"] {
            background-color: #f5f5f5 !important;
        }

        .stButton>button {
            background-color: #e8e8e8 !important;
            color: #222222 !important;
            border: 1px solid #ccc !important;
            border-radius: 6px !important;
        }
        .stButton>button:hover {
            background-color: #dcdcdc !important;
        }

        input, textarea, select {
            background-color: #fafafa !important;
            color: #222222 !important;
            border: 1px solid #ccc !important;
        }

        .app-card {
            background-color: #fafafa !important;
            border-radius: 14px;
            padding: 20px;
            border: 1px solid #ddd !important;
            box-shadow: 0 0 12px rgba(0,0,0,0.08) !important;
        }

        h1, h2, h3, h4 {
            color: #009944 !important;
            font-weight: 600;
        }

        .status-ok { color: #009944 !important; font-weight: bold; }
        .status-down { color: #cc0000 !important; font-weight: bold; }
        .status-warn { color: #cc8800 !important; font-weight: bold; }

        </style>
        """,
        unsafe_allow_html=True,
    )
