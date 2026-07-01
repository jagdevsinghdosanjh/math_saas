import streamlit as st
from typing import Any, Dict, List

from utils.db import get_supabase
from auth import require_admin, TEXT_MUTED


# ---------------------------------------------------------
# ADD NEW CONTENT
# ---------------------------------------------------------
def _publish_content(sb) -> None:
    st.subheader("Add New Content")

    with st.form("publish_content_form"):
        title = st.text_input("Title")
        body = st.text_area("Content", height=200)
        is_premium = st.checkbox("Premium (Subscribers Only)")
        submit = st.form_submit_button("Publish")

        if submit:
            admin = st.session_state.get("admin")
            admin_id = admin["id"] if isinstance(admin, dict) else None

            if not admin_id:
                st.error("Admin session invalid.")
                return

            title_clean = (title or "").strip()
            body_clean = (body or "").strip()

            if not title_clean or not body_clean:
                st.error("Title and content cannot be empty.")
                return

            try:
                sb.table("public_content").insert(
                    {
                        "title": title_clean,
                        "body": body_clean,
                        "is_premium": is_premium,
                        "created_by": admin_id,
                    }
                ).execute()

                st.success("Content published successfully.")
                st.rerun()

            except Exception as exc:
                st.error(f"Failed to publish content: {exc}")


# ---------------------------------------------------------
# FETCH EXISTING CONTENT
# ---------------------------------------------------------
def _fetch_content(sb) -> List[Dict[str, Any]]:
    try:
        res = (
            sb.table("public_content")
            .select("id, title, body, is_premium, created_at, created_by")
            .order("created_at", desc=True)
            .execute()
        )
        raw = res.data or []
        return [item for item in raw if isinstance(item, dict)]

    except Exception as exc:
        st.error(f"Error fetching content: {exc}")
        return []


# ---------------------------------------------------------
# RENDER A SINGLE CONTENT CARD
# ---------------------------------------------------------
def _render_item(sb, item: Dict[str, Any]) -> None:
    item_id = item.get("id")
    item_title = item.get("title", "Untitled")
    item_body = item.get("body", "")
    item_premium = item.get("is_premium", False)

    st.markdown(
        f"""
        <div class="neon-card" style="margin-bottom:16px;">
            <h4>{item_title}</h4>
            <p style="color:{TEXT_MUTED}; white-space:pre-wrap;">{item_body}</p>
            <p><strong>Premium:</strong> {item_premium}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not item_id:
        return

    delete_key = f"delete_{item_id}"

    if st.button("Delete", key=delete_key):
        try:
            sb.table("public_content").delete().eq("id", item_id).execute()
            st.success(f"Deleted '{item_title}'.")
            st.rerun()
        except Exception as exc:
            st.error(f"Failed to delete content: {exc}")


# ---------------------------------------------------------
# MAIN ADMIN PAGE
# ---------------------------------------------------------
def render() -> None:
    require_admin()
    st.title("📚 Content Manager")

    sb = get_supabase()

    # Fetch content
    res = (
        sb.table("public_content")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    items = res.data or []

    if not items:
        st.info("No content found.")
        return

    # Display content list
    st.subheader("All Content")
    st.dataframe(items, hide_index=True, width="stretch")

    # Add new content
    st.subheader("Add New Content")

    with st.form("add_content_form"):
        title = st.text_input("Title")
        body = st.text_area("Body")

        submit = st.form_submit_button("Create")

        if submit:
            try:
                sb.table("content").insert(
                    {"title": title, "body": body}
                ).execute()

                st.success("Content created successfully.")
                st.rerun()
            except Exception as exc:
                st.error(f"Failed to create content: {exc}")

# def render() -> None:
#     require_admin()
#     sb = get_supabase()

#     st.title("Content Manager")

#     # Add new content
#     _publish_content(sb)

#     # Existing content
#     st.subheader("Existing Content")
#     items = _fetch_content(sb)

#     if not items:
#         st.info("No content available.")
#         return

#     for item in items:
#         _render_item(sb, item)
