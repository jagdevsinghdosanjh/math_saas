import streamlit as st

# -----------------------------
# DARK NEON THEME
# -----------------------------
def apply_dark_theme():
    st.markdown(
        """
        <style>
        body {
            background: radial-gradient(circle at 20% 20%, #0f1115, #050608 60%);
            color: #f8f9fa;
            font-family: 'Inter', sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------
# LIGHT THEME
# -----------------------------
def apply_light_theme():
    st.markdown(
        """
        <style>
        body {
            background-color: #ffffff;
            color: #000000;
            font-family: 'Inter', sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
