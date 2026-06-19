import streamlit as st

from admin.sync_chapters import sync_chapters
from auth import require_admin, logout, top_bar

from admin.analytics import render as render_analytics
from admin.subscriptions_admin import render as render_subscriptions
from admin.billing import render as render_billing
from admin.chapters import render as render_chapters
from admin.users import render as render_users
from admin.pdf_notes import render as render_pdf_notes
from admin.videos import render as render_videos
from admin.content_admin import render as render_content_admin
from admin.settings import render as render_settings


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
