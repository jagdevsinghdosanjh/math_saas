import streamlit as st
from math_saas.utils.db import get_supabase
from math_saas.auth import require_admin, TEXT_MUTED


def render():
    """Render the Admin Content Manager panel."""
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

        if not admin_id:
            st.error("Admin session invalid.")
            return

        try:
            sb.table("public_content").insert(
                {
                    "title": title.strip(),
                    "body": body.strip(),
                    "is_premium": is_premium,
                    "created_by": admin_id,
                }
            ).execute()
            st.success("✅ Content published successfully.")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to publish content: {e}")

    # -----------------------------
    # EXISTING CONTENT
    # -----------------------------
    st.subheader("Existing Content")

    try:
        res = sb.table("public_content").select("*").order("created_at", desc=True).execute()
        items_raw = res.data or []
    except Exception as e:
        st.error(f"Error fetching content: {e}")
        return

    items = [i for i in items_raw if isinstance(i, dict)]

    if not items:
        st.info("No content available.")
        return

    for item in items:
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

        if item_id and st.button(f"Delete {item_title}"):
            try:
                sb.table("public_content").delete().eq("id", item_id).execute()
                st.success(f"Deleted '{item_title}'.")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to delete content: {e}")

# import streamlit as st
# from math_saas.utils.db import get_supabase
# from math_saas.auth import require_admin, TEXT_MUTED #noqa


# def render():
#     require_admin()
#     sb = get_supabase()

#     st.title("Content Manager")

#     # -----------------------------
#     # ADD NEW CONTENT
#     # -----------------------------
#     st.subheader("Add New Content")

#     title = st.text_input("Title")
#     body = st.text_area("Content", height=200)
#     is_premium = st.checkbox("Premium (Subscribers Only)")

#     if st.button("Publish"):
#         admin = st.session_state.get("admin")
#         admin_id = admin["id"] if isinstance(admin, dict) else None

#         if admin_id:
#             sb.table("public_content").insert(
#                 {
#                     "title": title,
#                     "body": body,
#                     "is_premium": is_premium,
#                     "created_by": admin_id,
#                 }
#             ).execute()

#             st.success("Content published.")
#             st.rerun()
#         else:
#             st.error("Admin session invalid.")

#     # -----------------------------
#     # EXISTING CONTENT
#     # -----------------------------
#     st.subheader("Existing Content")

#     res = sb.table("public_content").select("*").order("created_at", desc=True).execute()
#     items_raw = res.data or []

#     # Ensure items are dicts
#     items = [i for i in items_raw if isinstance(i, dict)]

#     if not items:
#         st.info("No content available.")
#         return

#     for item in items:
#         item_id = item.get("id")
#         item_title = item.get("title", "Untitled")
#         item_premium = item.get("is_premium", False)

#         st.markdown(f"### {item_title}")
#         st.markdown(f"**Premium:** {item_premium}")

#         if item_id and st.button(f"Delete {item_id}"):
#             sb.table("public_content").delete().eq("id", item_id).execute()
#             st.rerun()
