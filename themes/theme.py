import streamlit as st

# -----------------------------
# DARK NEON THEME (FIXED)
# -----------------------------
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

        /* FIX: All text elements */
        p, span, label, h1, h2, h3, h4, h5, h6, div, .stMarkdown, .stText, .stRadio label {
            color: #f8f9fa !important;
        }

        /* FIX: Streamlit metric cards */
        .stMetric, .metric-card, [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
            color: #f8f9fa !important;
        }

        /* FIX: Buttons */
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

        /* FIX: Inputs */
        input, textarea {
            background-color: #1a1d23 !important;
            color: #f8f9fa !important;
            border: 1px solid #333 !important;
        }

        /* FIX: Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #0d0f12 !important;
        }

        /* FIX: Status colors */
        .status-ok {
            color: #00ff88 !important;
            font-weight: bold;
        }
        .status-down {
            color: #ff4d4d !important;
            font-weight: bold;
        }
        .status-warn {
            color: #ffcc00 !important;
            font-weight: bold;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------
# LIGHT THEME (FIXED)
# -----------------------------
def apply_light_theme():
    st.markdown(
        """
        <style>

        body, .stApp {
            background-color: #ffffff !important;
            color: #000000 !important;
            font-family: 'Inter', sans-serif;
        }

        p, span, label, h1, h2, h3, h4, h5, h6, div, .stMarkdown, .stText {
            color: #000000 !important;
        }

        section[data-testid="stSidebar"] {
            background-color: #f5f5f5 !important;
        }

        .stButton>button {
            background-color: #e8e8e8 !important;
            color: #000000 !important;
            border: 1px solid #ccc !important;
            border-radius: 6px !important;
        }
        .stButton>button:hover {
            background-color: #dcdcdc !important;
        }

        .metric-card {
            background-color: #fafafa !important;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #ddd !important;
            color: #000000 !important;
        }

        .status-ok {
            color: #009944 !important;
            font-weight: bold;
        }
        .status-down {
            color: #cc0000 !important;
            font-weight: bold;
        }
        .status-warn {
            color: #cc8800 !important;
            font-weight: bold;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
