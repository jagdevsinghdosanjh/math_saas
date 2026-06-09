import streamlit as st

from math_saas.admin.sync_chapters import sync_chapters
from math_saas.auth import require_admin, logout, top_bar

from math_saas.admin.analytics import render as render_analytics
from math_saas.admin.subscriptions_admin import render as render_subscriptions
from math_saas.admin.billing import render as render_billing
from math_saas.admin.chapters import render as render_chapters
from math_saas.admin.users import render as render_users
from math_saas.admin.pdf_notes import render as render_pdf_notes
from math_saas.admin.videos import render as render_videos
from math_saas.admin.content_admin import render as render_content_admin
from math_saas.admin.settings import render as render_settings


# -------------------------------------------------
# ADMIN SYNC BUTTON
# -------------------------------------------------
def render_admin_sync() -> None:
    st.subheader("🔄 Sync CBSE Chapters to Supabase")

    if st.button("Start Sync", key="btn_sync_chapters"):
        with st.spinner("Syncing chapters..."):
            try:
                sync_chapters()
                st.success("✅ Chapters synced successfully!")
            except Exception as exc:
                st.error(f"❌ Sync failed: {exc}")


# -------------------------------------------------
# MAIN ADMIN PANEL
# -------------------------------------------------
def run_admin() -> None:
    require_admin()

    # Logout via query params
    params = st.query_params
    if params.get("admin_logout") == "true":
        logout()

    # Top bar
    top_bar("Math Hub Admin Panel", "Admin", "admin_logout")

    # Sidebar navigation
    st.sidebar.markdown("### Navigation")

    nav_items = [
        "Analytics",
        "Subscriptions",
        "Billing",
        "Chapters",
        "Users",
        "PDF Notes",
        "Videos",
        "Content Manager",
        "Settings",
        "Sync Chapters",
    ]

    menu = st.sidebar.radio(
        "Select section",
        nav_items,
        label_visibility="collapsed",
        key="admin_menu_radio",
    )

    routes = {
        "Analytics": render_analytics,
        "Subscriptions": render_subscriptions,
        "Billing": render_billing,
        "Chapters": render_chapters,
        "Users": render_users,
        "PDF Notes": render_pdf_notes,
        "Videos": render_videos,
        "Content Manager": render_content_admin,
        "Settings": render_settings,
        "Sync Chapters": render_admin_sync,
    }

    try:
        routes.get(menu, render_analytics)()
    except Exception as exc:
        st.error(f"Error loading section: {exc}")

# import streamlit as st

# from math_saas.admin.sync_chapters import sync_chapters
# from math_saas.auth import require_admin, logout, top_bar
# from math_saas.admin.analytics import render as render_analytics
# from math_saas.admin.subscriptions_admin import render as render_subscriptions
# from math_saas.admin.billing import render as render_billing
# from math_saas.admin.chapters import render as render_chapters
# from math_saas.admin.users import render as render_users
# from math_saas.admin.pdf_notes import render as render_pdf_notes
# from math_saas.admin.videos import render as render_videos
# from math_saas.admin.content_admin import render as render_content_admin
# from math_saas.admin.settings import render as render_settings


# # -------------------------------------------------
# # ADMIN SYNC BUTTON
# # -------------------------------------------------
# def render_admin_sync() -> None:
#     """Admin tool to sync CBSE chapters into Supabase."""
#     st.subheader("🔄 Sync CBSE Chapters to Supabase")

#     if st.button("Start Sync", key="btn_sync_chapters"):
#         with st.spinner("Syncing chapters..."):
#             try:
#                 sync_chapters()
#                 st.success("✅ Chapters synced successfully into Supabase!")
#             except Exception as exc:
#                 st.error(f"❌ Sync failed: {exc}")


# # -------------------------------------------------
# # MAIN ADMIN PANEL
# # -------------------------------------------------
# def run_admin() -> None:
#     """Main entry point for the Admin Panel."""
#     require_admin()

#     admin = st.session_state.get("admin")
#     if not admin:
#         st.error("Admin session missing. Please log in again.")
#         return

#     # Logout via query params (handled here for safety)
#     params = st.query_params
#     if params.get("admin_logout") == "true":
#         logout()

#     # Top bar
#     top_bar("Math Hub Admin Panel", "Admin", "admin_logout")

#     # Sidebar navigation
#     st.sidebar.markdown("### Navigation")

#     nav_items = [
#         "Analytics",
#         "Subscriptions",
#         "Billing",
#         "Chapters",
#         "Users",
#         "PDF Notes",
#         "Videos",
#         "Content Manager",
#         "Settings",
#         "Sync Chapters",
#     ]

#     menu = st.sidebar.radio(
#         "Select section",
#         nav_items,
#         label_visibility="collapsed",
#         key="admin_menu_radio",
#     )

#     routes = {
#         "Analytics": render_analytics,
#         "Subscriptions": render_subscriptions,
#         "Billing": render_billing,
#         "Chapters": render_chapters,
#         "Users": render_users,
#         "PDF Notes": render_pdf_notes,
#         "Videos": render_videos,
#         "Content Manager": render_content_admin,
#         "Settings": render_settings,
#         "Sync Chapters": render_admin_sync,
#     }

#     try:
#         routes.get(menu, render_analytics)()
#     except Exception as exc:
#         st.error(f"Error loading section: {exc}")

# # import streamlit as st
# # from math_saas.admin.sync_chapters import sync_chapters

# # from math_saas.auth import (
# #     require_admin,
# #     logout,
# #     top_bar,
# # )

# # from math_saas.admin.analytics import render as render_analytics
# # from math_saas.admin.subscriptions_admin import render as render_subscriptions
# # from math_saas.admin.billing import render as render_billing
# # from math_saas.admin.chapters import render as render_chapters
# # from math_saas.admin.users import render as render_users
# # from math_saas.admin.pdf_notes import render as render_pdf_notes
# # from math_saas.admin.videos import render as render_videos
# # from math_saas.admin.content_admin import render as render_content_admin
# # from math_saas.admin.settings import render as render_settings


# # # -------------------------------------------------
# # # ADMIN SYNC BUTTON
# # # -------------------------------------------------
# # def render_admin_sync():
# #     """Admin tool to sync CBSE chapters into Supabase."""
# #     st.subheader("🔄 Sync CBSE Chapters to Supabase")

# #     if st.button("Start Sync", key="btn_sync_chapters"):
# #         with st.spinner("Syncing chapters..."):
# #             try:
# #                 sync_chapters()
# #                 st.success("✅ Chapters synced successfully into Supabase!")
# #             except Exception as e:
# #                 st.error(f"❌ Sync failed: {e}")


# # # -------------------------------------------------
# # # MAIN ADMIN PANEL
# # # -------------------------------------------------
# # def run_admin():
# #     """Main entry point for the Admin Panel."""
# #     require_admin()

# #     admin = st.session_state.get("admin")
# #     if not admin:
# #         st.error("Admin session missing. Please log in again.")
# #         return

# #     # Safe logout via query params
# #     params = st.query_params
# #     if params.get("admin_logout") == "true":
# #         logout()

# #     # Top bar
# #     top_bar("Math Hub Admin Panel", "Admin", "admin_logout")

# #     # Sidebar navigation
# #     st.sidebar.markdown("### Navigation")

# #     NAV_ITEMS = [
# #         "Analytics",
# #         "Subscriptions",
# #         "Billing",
# #         "Chapters",
# #         "Users",
# #         "PDF Notes",
# #         "Videos",
# #         "Content Manager",
# #         "Settings",
# #         "Sync Chapters",
# #     ]

# #     menu = st.sidebar.radio(
# #         "Select section",
# #         NAV_ITEMS,
# #         label_visibility="collapsed",
# #         key="admin_menu_radio"
# #     )

# #     ROUTES = {
# #         "Analytics": render_analytics,
# #         "Subscriptions": render_subscriptions,
# #         "Billing": render_billing,
# #         "Chapters": render_chapters,
# #         "Users": render_users,
# #         "PDF Notes": render_pdf_notes,
# #         "Videos": render_videos,
# #         "Content Manager": render_content_admin,
# #         "Settings": render_settings,
# #         "Sync Chapters": render_admin_sync,
# #     }

# #     # Render selected page safely
# #     try:
# #         ROUTES.get(menu, render_analytics)()
# #     except Exception as e:
# #         st.error(f"Error loading section: {e}")

# # # import streamlit as st
# # # from math_saas.admin.sync_chapters import sync_chapters

# # # from math_saas.auth import (
# # #     require_admin,
# # #     logout,
# # #     top_bar,
# # # )

# # # from math_saas.admin.analytics import render as render_analytics
# # # from math_saas.admin.subscriptions_admin import render as render_subscriptions
# # # from math_saas.admin.billing import render as render_billing
# # # from math_saas.admin.chapters import render as render_chapters
# # # from math_saas.admin.users import render as render_users
# # # from math_saas.admin.pdf_notes import render as render_pdf_notes
# # # from math_saas.admin.videos import render as render_videos
# # # from math_saas.admin.content_admin import render as render_content_admin
# # # from math_saas.admin.settings import render as render_settings


# # # # -----------------------------
# # # # ADMIN SYNC BUTTON
# # # # -----------------------------
# # # def render_admin_sync():
# # #     """Admin tool to sync CBSE chapters into Supabase."""
# # #     st.subheader("🔄 Sync CBSE Chapters to Supabase")

# # #     if st.button("Start Sync"):
# # #         with st.spinner("Syncing chapters..."):
# # #             try:
# # #                 sync_chapters()
# # #                 st.success("✅ Chapters synced successfully into Supabase!")
# # #             except Exception as e:
# # #                 st.error(f"❌ Sync failed: {e}")


# # # # -----------------------------
# # # # MAIN ADMIN PANEL
# # # # -----------------------------
# # # def run_admin():
# # #     """Main entry point for the Admin Panel."""
# # #     require_admin()
# # #     st.write("AUTH UID:", st.session_state["admin"]["id"])
# # #     # Safe query param access
# # #     params = st.query_params
# # #     if isinstance(params, dict) and params.get("admin_logout") == "true":
# # #         logout()

# # #     # Top bar
# # #     top_bar("Math Hub Admin Panel", "Admin", "admin_logout")

# # #     # Sidebar navigation
# # #     st.sidebar.markdown("### Navigation")

# # #     NAV_ITEMS = [
# # #         "Analytics",
# # #         "Subscriptions",
# # #         "Billing",
# # #         "Chapters",
# # #         "Users",
# # #         "PDF Notes",
# # #         "Videos",
# # #         "Content Manager",
# # #         "Settings",
# # #         "Sync Chapters",  # ✅ fixed spelling
# # #     ]

# # #     menu = st.sidebar.radio(
# # #         "Select section",
# # #         NAV_ITEMS,
# # #         label_visibility="collapsed",
# # #     )

# # #     # Route mapping
# # #     ROUTES = {
# # #         "Analytics": render_analytics,
# # #         "Subscriptions": render_subscriptions,
# # #         "Billing": render_billing,
# # #         "Chapters": render_chapters,
# # #         "Users": render_users,
# # #         "PDF Notes": render_pdf_notes,
# # #         "Videos": render_videos,
# # #         "Content Manager": render_content_admin,
# # #         "Settings": render_settings,
# # #         "Sync Chapters": render_admin_sync,  # ✅ fixed route
# # #     }

# # #     # Render selected page safely
# # #     try:
# # #         ROUTES.get(menu, render_analytics)()
# # #     except Exception as e:
# # #         st.error(f"Error loading section: {e}")
