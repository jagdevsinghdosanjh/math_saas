import streamlit as st
from math_saas.utils.db import get_supabase
from math_saas.auth import require_admin, TEXT_MUTED #noqa


def render():
    require_admin()
    sb = get_supabase()

    st.title("Content Manager")

    # -----------------------------
    # ADD NEW CONTENT
    # -----------------------------
    st.subheader("Add New Content")

    title = st.text_input("Title")
    body = st.text_area("Content", height=200)
    is_premium = st.checkbox("Premium (Subscribers Only)")

    if st.button("Publish"):
        admin = st.session_state.get("admin")
        admin_id = admin["id"] if isinstance(admin, dict) else None

        if admin_id:
            sb.table("public_content").insert(
                {
                    "title": title,
                    "body": body,
                    "is_premium": is_premium,
                    "created_by": admin_id,
                }
            ).execute()

            st.success("Content published.")
            st.rerun()
        else:
            st.error("Admin session invalid.")

    # -----------------------------
    # EXISTING CONTENT
    # -----------------------------
    st.subheader("Existing Content")

    res = sb.table("public_content").select("*").order("created_at", desc=True).execute()
    items_raw = res.data or []

    # Ensure items are dicts
    items = [i for i in items_raw if isinstance(i, dict)]

    if not items:
        st.info("No content available.")
        return

    for item in items:
        item_id = item.get("id")
        item_title = item.get("title", "Untitled")
        item_premium = item.get("is_premium", False)

        st.markdown(f"### {item_title}")
        st.markdown(f"**Premium:** {item_premium}")

        if item_id and st.button(f"Delete {item_id}"):
            sb.table("public_content").delete().eq("id", item_id).execute()
            st.rerun()
