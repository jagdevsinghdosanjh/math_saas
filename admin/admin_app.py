import streamlit as st

from auth import require_admin, logout, top_bar
from admin.sync_chapters import sync_chapters

from utils.health import health_check, run_health_monitor, host_ram_monitor

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
# HEALTH MONITOR PAGE
# -------------------------------------------------
def render_health_monitor() -> None:
    st.title("🔍 System Health")

    auto_refresh = st.checkbox("Auto-refresh every 10 seconds", value=False)
    if auto_refresh:
        st.rerun()

    results = health_check()

    def badge(ok: bool) -> str:
        return (
            "<span style='color:#00c853; font-weight:bold;'>🟢 OK</span>"
            if ok else
            "<span style='color:#d50000; font-weight:bold;'>🔴 DOWN</span>"
        )

    # API Status
    st.markdown("## 🌐 API Status")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div style="padding:12px; border-radius:8px; background:#1e1e1e;">
                <h4>Local API</h4>
                {badge(bool(results["local_api"]))}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div style="padding:12px; border-radius:8px; background:#1e1e1e;">
                <h4>Tunnel API</h4>
                {badge(bool(results["tunnel_api"]))}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Model Status
    st.markdown("## 🤖 Model Status")

    model_cards = [
        ("DeepSeek 1.5B", bool(results["deepseek_1_5b"]), results["deepseek_1_5b_latency"]),
        ("DeepSeek 7B", bool(results["deepseek_7b"]), results["deepseek_7b_latency"]),
        ("Llama 3.2", bool(results["llama_3_2"]), results["llama_3_2_latency"]),
    ]

    colA, colB, colC = st.columns(3)

    for (name, ok, latency), col in zip(model_cards, [colA, colB, colC]):
        safe_latency = latency if isinstance(latency, int) else 0
        bar_width = min(safe_latency, 3000) / 30

        col.markdown(
            f"""
            <div style="padding:14px; border-radius:10px; background:#1e1e1e;">
                <h4>{name}</h4>
                {badge(ok)}
                <p style="margin-top:6px;">⏱ Latency:
                    <strong>{safe_latency if safe_latency else 'N/A'} ms</strong>
                </p>
                <div style="height:8px; background:#333; border-radius:4px;">
                    <div style="
                        width:{bar_width}%;
                        height:100%;
                        background:{'#00e676' if ok else '#ff1744'};
                        border-radius:4px;">
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Summary
    st.markdown("## 📊 Summary")
    st.write(
        f"""
        - **APIs Online:** {badge(bool(results["tunnel_api"]))}
        - **Models Healthy:** {badge(bool(results["deepseek_1_5b"] and results["deepseek_7b"]))}
        - **Summary Engine:** {badge(bool(results["llama_3_2"]))}
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Rhino Host RAM
    st.markdown("# 🖥️ Rhino Host - Status")

    ram = host_ram_monitor(base_url="http://192.168.1.2:5055")

    if "error" not in ram:
        st.metric("Host Total RAM", f"{ram['total_gb']} GB")
        st.metric("Host Used RAM", f"{ram['used_gb']} GB")
        st.metric("Host Free RAM", f"{ram['free_gb']} GB")
    else:
        st.error(f"Unable to read host RAM: {ram['error']}")

    st.markdown("---")

    # Container Health
    run_health_monitor()


# -------------------------------------------------
# SYNC BUTTON
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

    params = st.query_params
    if params.get("admin_logout") == "true":
        logout()
        return

    top_bar("Math Hub Admin Panel", "Admin", "admin_logout")

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
        "Health Monitor",
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
        "Health Monitor": render_health_monitor,
    }

    handler = routes.get(menu)
    if handler:
        try:
            handler()
        except Exception as exc:
            st.error(f"Error loading section: {exc}")
    else:
        st.error("Invalid admin section selected.")
