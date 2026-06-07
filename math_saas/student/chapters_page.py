import streamlit as st
from auth import TEXT_MUTED


def render_chapters_page():
    st.markdown(
        """
        <h3 style="margin-top:0;">Chapters</h3>
        <p style="color:#9ca3af; margin-top:-8px;">
            Your chapter list will appear here soon.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="neon-card">
            <h4 style="margin:0;">Coming Soon</h4>
            <p style="color:{TEXT_MUTED}; margin:4px 0 0 0;">
                The chapters module will include:
            </p>
            <ul style="color:{TEXT_MUTED}; margin-top:6px;">
                <li>Chapter list</li>
                <li>Progress tracking</li>
                <li>Locked/unlocked chapters</li>
                <li>Notes & videos</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
