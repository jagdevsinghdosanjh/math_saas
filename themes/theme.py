import streamlit as st

# ============================================================
# DARK NEON THEME (FULL READABILITY)
# ============================================================
def apply_dark_theme():
    st.markdown(
        """
        <style>

        /* GLOBAL BACKGROUND */
        body, .stApp {
            background: radial-gradient(circle at 20% 20%, #0f1115, #050608 60%) !important;
            color: #f8f9fa !important;
            font-family: 'Inter', sans-serif;
        }

        /* UNIVERSAL TEXT FIX */
        p, span, label, h1, h2, h3, h4, h5, h6, div, 
        .stMarkdown, .stText, .stRadio label, .stSelectbox label {
            color: #f8f9fa !important;
        }

        /* NAVBAR + USERNAME FIX */
        header, [data-testid="stHeader"], .st-emotion-cache-18ni7ap {
            background-color: transparent !important;
            color: #f8f9fa !important;
        }

        /* Logged-in user badge */
        .user-badge {
            padding: 6px 12px;
            background-color: #1a1d23 !important;
            color: #f8f9fa !important;
            border-radius: 6px;
            border: 1px solid #333 !important;
        }

        /* BUTTONS */
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

        /* INPUTS */
        input, textarea, select {
            background-color: #1a1d23 !important;
            color: #f8f9fa !important;
            border: 1px solid #333 !important;
        }

        /* SIDEBAR */
        section[data-testid="stSidebar"] {
            background-color: #0d0f12 !important;
        }

        /* CARDS / METRICS */
        .metric-card, .stMetric, [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
            color: #f8f9fa !important;
        }

        /* STATUS COLORS */
        .status-ok { color: #00ff88 !important; font-weight: bold; }
        .status-down { color: #ff4d4d !important; font-weight: bold; }
        .status-warn { color: #ffcc00 !important; font-weight: bold; }

        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# LIGHT THEME (FULL READABILITY)
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

        /* UNIVERSAL TEXT FIX */
        p, span, label, h1, h2, h3, h4, h5, h6, div, 
        .stMarkdown, .stText, .stRadio label, .stSelectbox label {
            color: #222222 !important;
        }

        /* NAVBAR + USERNAME FIX */
        header, [data-testid="stHeader"], .st-emotion-cache-18ni7ap {
            background-color: transparent !important;
            color: #222222 !important;
        }

        /* Logged-in user badge */
        .user-badge {
            padding: 6px 12px;
            background-color: #f0f0f0 !important;
            color: #222222 !important;
            border-radius: 6px;
            border: 1px solid #ccc !important;
        }

        /* BUTTONS */
        .stButton>button {
            background-color: #e8e8e8 !important;
            color: #222222 !important;
            border: 1px solid #ccc !important;
            border-radius: 6px !important;
        }
        .stButton>button:hover {
            background-color: #dcdcdc !important;
        }

        /* INPUTS */
        input, textarea, select {
            background-color: #fafafa !important;
            color: #222222 !important;
            border: 1px solid #ccc !important;
        }

        /* SIDEBAR */
        section[data-testid="stSidebar"] {
            background-color: #f5f5f5 !important;
        }

        /* CARDS / METRICS */
        .metric-card {
            background-color: #fafafa !important;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #ddd !important;
            color: #222222 !important;
        }

        /* STATUS COLORS */
        .status-ok { color: #009944 !important; font-weight: bold; }
        .status-down { color: #cc0000 !important; font-weight: bold; }
        .status-warn { color: #cc8800 !important; font-weight: bold; }

        </style>
        """,
        unsafe_allow_html=True,
    )
