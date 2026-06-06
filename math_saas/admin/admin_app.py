import streamlit as st
from math_saas.admin.content_admin import render as render_content_admin

from math_saas.auth import (
    require_admin,
    logout,
    app_container_style,
    top_bar,
)

from math_saas.admin.subscriptions_admin import render as render_subscriptions
from math_saas.admin.analytics import render as render_analytics
from math_saas.admin.billing import render as render_billing
from math_saas.admin.chapters import render as render_chapters
from math_saas.admin.users import render as render_users
from math_saas.admin.pdf_notes import render as render_pdf_notes
from math_saas.admin.videos import render as render_videos
from math_saas.admin.settings import render as render_settings


def run_admin():
    app_container_style()

    # SAFE QUERY PARAM ACCESS
    params = st.query_params
    admin_logout_flag = params["admin_logout"] if "admin_logout" in params else None

    if admin_logout_flag == "true":
        logout()

    require_admin()
    top_bar("Math Hub Admin Panel", "Admin", "admin_logout")

    with st.sidebar:
        st.markdown("### Navigation")
        menu = st.radio(
            "",
            [
                "Analytics",
                "Subscriptions",
                "Billing",
                "Chapters",
                "Users",
                "PDF Notes",
                "Videos",
                "Content Manager",
                "Settings",
            ],
        )

    if menu == "Analytics":
        render_analytics()

    elif menu == "Subscriptions":
        render_subscriptions()

    elif menu == "Billing":
        render_billing()

    elif menu == "Chapters":
        render_chapters()

    elif menu == "Users":
        render_users()

    elif menu == "PDF Notes":
        render_pdf_notes()

    elif menu == "Videos":
        render_videos()

    elif menu == "Content Manager":
        render_content_admin()

    elif menu == "Settings":
        render_settings()
