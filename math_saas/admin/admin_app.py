import streamlit as st

from math_saas.auth import (
    require_admin,
    logout,
    top_bar,
)

from math_saas.admin.analytics import render as render_analytics
from math_saas.admin.subscriptions_admin import render as render_subscriptions
from math_saas.admin.billing import render as render_billing
from math_saas.admin.chapters import render as render_chapters
from math_saas.admin.users import render as render_users
from math_saas.admin.pdf_notes import render as render_pdf_notes
from math_saas.admin.videos import render as render_videos
from math_saas.admin.content_admin import render as render_content_admin
from math_saas.admin.settings import render as render_settings


# -----------------------------
# MAIN ADMIN PANEL
# -----------------------------
def run_admin():
    """Main entry point for the Admin Panel."""
    # Authentication
    require_admin()

    # Safe query param access
    params = st.query_params
    if params.get("admin_logout") == "true":
        logout()

    # Top bar
    top_bar("Math Hub Admin Panel", "Admin", "admin_logout")

    # Sidebar navigation
    st.sidebar.markdown("### Navigation")

    NAV_ITEMS = [
        "Analytics",
        "Subscriptions",
        "Billing",
        "Chapters",
        "Users",
        "PDF Notes",
        "Videos",
        "Content Manager",
        "Settings",
    ]

    menu = st.sidebar.radio(
        "Select section",
        NAV_ITEMS,
        label_visibility="collapsed",
    )

    # Route mapping
    ROUTES = {
        "Analytics": render_analytics,
        "Subscriptions": render_subscriptions,
        "Billing": render_billing,
        "Chapters": render_chapters,
        "Users": render_users,
        "PDF Notes": render_pdf_notes,
        "Videos": render_videos,
        "Content Manager": render_content_admin,
        "Settings": render_settings,
    }

    # Render selected page
    ROUTES.get(menu, render_analytics)()

# import streamlit as st

# from math_saas.auth import (
#     require_admin,
#     logout,
#     app_container_style,
#     top_bar,
# )

# from math_saas.admin.analytics import render as render_analytics
# from math_saas.admin.subscriptions_admin import render as render_subscriptions
# from math_saas.admin.billing import render as render_billing
# from math_saas.admin.chapters import render as render_chapters
# from math_saas.admin.users import render as render_users
# from math_saas.admin.pdf_notes import render as render_pdf_notes
# from math_saas.admin.videos import render as render_videos
# from math_saas.admin.content_admin import render as render_content_admin
# from math_saas.admin.settings import render as render_settings


# def run_admin():
#     """Main entry point for the Admin Panel."""
#     app_container_style()

#     # Safe query param access
#     params = st.query_params
#     if params.get("admin_logout") == "true":
#         logout()

#     # Authentication
#     require_admin()

#     # Top bar
#     top_bar("Math Hub Admin Panel", "Admin", "admin_logout")

#     # Navigation items
#     NAV_ITEMS = [
#         "Analytics",
#         "Subscriptions",
#         "Billing",
#         "Chapters",
#         "Users",
#         "PDF Notes",
#         "Videos",
#         "Content Manager",
#         "Settings",
#     ]

#     # Sidebar navigation
#     with st.sidebar:
#         st.markdown("### Navigation")
#         menu = st.radio(
#             "Select section",
#             NAV_ITEMS,
#             label_visibility="collapsed",
#         )

#     # Route mapping
#     ROUTES = {
#         "Analytics": render_analytics,
#         "Subscriptions": render_subscriptions,
#         "Billing": render_billing,
#         "Chapters": render_chapters,
#         "Users": render_users,
#         "PDF Notes": render_pdf_notes,
#         "Videos": render_videos,
#         "Content Manager": render_content_admin,
#         "Settings": render_settings,
#     }

#     # Render selected page
#     ROUTES[menu]()
