import streamlit as st
from math_saas.utils.db import get_supabase
from math_saas.auth import require_admin, TEXT_MUTED


def _publish_content(sb) -> None:
    """Form to add new public content."""
    st.subheader("Add New Content")

    title = st.text_input("Title")
    body = st.text_area("Content", height=200)
    is_premium = st.checkbox("Premium (Subscribers Only)")

    if st.button("Publish", key="publish_btn"):
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
            (
                sb.table("public_content")
                .insert(
                    {
                        "title": title_clean,
                        "body": body_clean,
                        "is_premium": is_premium,
                        "created_by": admin_id,
                    }
                )
                .execute()
            )
            st.success("✅ Content published successfully.")
            st.rerun()
        except Exception as exc:  # noqa: BLE001
            st.error(f"Failed to publish content: {exc}")


def _fetch_content(sb):
    """Fetch existing public content items."""
    try:
        res = (
            sb.table("public_content")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )
        items_raw = res.data or []
    except Exception as exc:  # noqa: BLE001
        st.error(f"Error fetching content: {exc}")
        return []

    return [item for item in items_raw if isinstance(item, dict)]


def _render_item(sb, item: dict) -> None:
    """Render a single content item card with actions."""
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

    cols = st.columns([1, 1])
    delete_key = f"delete_{item_id}"

    with cols[1]:
        if st.button("Delete", key=delete_key):
            try:
                (
                    sb.table("public_content")
                    .delete()
                    .eq("id", item_id)
                    .execute()
                )
                st.success(f"Deleted '{item_title}'.")
                st.rerun()
            except Exception as exc:  # noqa: BLE001
                st.error(f"Failed to delete content: {exc}")


def render() -> None:
    """Render the Admin Content Manager panel."""
    require_admin()
    sb = get_supabase()

    st.title("Content Manager")

    # Add new content
    _publish_content(sb)

    # Existing content
    st.subheader("Existing Content")
    items = _fetch_content(sb)

    if not items:
        st.info("No content available.")
        return

    for item in items:
        _render_item(sb, item)

# import streamlit as st
# from math_saas.utils.db import get_supabase
# from math_saas.auth import require_admin, TEXT_MUTED


# def render():
#     """Render the Admin Content Manager panel."""
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

#     if st.button("Publish", key="publish_btn"):
#         admin = st.session_state.get("admin")
#         admin_id = admin["id"] if isinstance(admin, dict) else None

#         if not admin_id:
#             st.error("Admin session invalid.")
#             return

#         try:
#             sb.table("public_content").insert(
#                 {
#                     "title": title.strip(),
#                     "body": body.strip(),
#                     "is_premium": is_premium,
#                     "created_by": admin_id,
#                 }
#             ).execute()
#             st.success("✅ Content published successfully.")
#             st.rerun()
#         except Exception as e:
#             st.error(f"Failed to publish content: {e}")

#     # -----------------------------
#     # EXISTING CONTENT
#     # -----------------------------
#     st.subheader("Existing Content")

#     try:
#         res = sb.table("public_content").select("*").order("created_at", desc=True).execute()
#         items_raw = res.data or []
#     except Exception as e:
#         st.error(f"Error fetching content: {e}")
#         return

#     items = [i for i in items_raw if isinstance(i, dict)]

#     if not items:
#         st.info("No content available.")
#         return

#     # -----------------------------
#     # RENDER EACH CONTENT ITEM
#     # -----------------------------
#     for item in items:
#         item_id = item.get("id")
#         item_title = item.get("title", "Untitled")
#         item_body = item.get("body", "")
#         item_premium = item.get("is_premium", False)

#         st.markdown(
#             f"""
#             <div class="neon-card" style="margin-bottom:16px;">
#                 <h4>{item_title}</h4>
#                 <p style="color:{TEXT_MUTED}; white-space:pre-wrap;">{item_body}</p>
#                 <p><strong>Premium:</strong> {item_premium}</p>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )

#         # UNIQUE KEY FIX
#         delete_key = f"delete_{item_id}"

#         if st.button(f"Delete", key=delete_key):
#             try:
#                 sb.table("public_content").delete().eq("id", item_id).execute()
#                 st.success(f"Deleted '{item_title}'.")
#                 st.rerun()
#             except Exception as e:
#                 st.error(f"Failed to delete content: {e}")

# # import streamlit as st
# # from math_saas.utils.db import get_supabase
# # from math_saas.auth import require_admin, TEXT_MUTED


# # def render():
# #     """Render the Admin Content Manager panel."""
# #     require_admin()
# #     sb = get_supabase()

# #     st.title("Content Manager")

# #     # -----------------------------
# #     # ADD NEW CONTENT
# #     # -----------------------------
# #     st.subheader("Add New Content")

# #     title = st.text_input("Title")
# #     body = st.text_area("Content", height=200)
# #     is_premium = st.checkbox("Premium (Subscribers Only)")

# #     if st.button("Publish"):
# #         admin = st.session_state.get("admin")
# #         admin_id = admin["id"] if isinstance(admin, dict) else None

# #         if not admin_id:
# #             st.error("Admin session invalid.")
# #             return

# #         try:
# #             sb.table("public_content").insert(
# #                 {
# #                     "title": title.strip(),
# #                     "body": body.strip(),
# #                     "is_premium": is_premium,
# #                     "created_by": admin_id,
# #                 }
# #             ).execute()
# #             st.success("✅ Content published successfully.")
# #             st.rerun()
# #         except Exception as e:
# #             st.error(f"Failed to publish content: {e}")

# #     # -----------------------------
# #     # EXISTING CONTENT
# #     # -----------------------------
# #     st.subheader("Existing Content")

# #     try:
# #         res = sb.table("public_content").select("*").order("created_at", desc=True).execute()
# #         items_raw = res.data or []
# #     except Exception as e:
# #         st.error(f"Error fetching content: {e}")
# #         return

# #     items = [i for i in items_raw if isinstance(i, dict)]

# #     if not items:
# #         st.info("No content available.")
# #         return

# #     for item in items:
# #         item_id = item.get("id")
# #         item_title = item.get("title", "Untitled")
# #         item_body = item.get("body", "")
# #         item_premium = item.get("is_premium", False)

# #         st.markdown(
# #             f"""
# #             <div class="neon-card" style="margin-bottom:16px;">
# #                 <h4>{item_title}</h4>
# #                 <p style="color:{TEXT_MUTED}; white-space:pre-wrap;">{item_body}</p>
# #                 <p><strong>Premium:</strong> {item_premium}</p>
# #             </div>
# #             """,
# #             unsafe_allow_html=True,
# #         )

# #         if item_id and st.button(f"Delete {item_title}"):
# #             try:
# #                 sb.table("public_content").delete().eq("id", item_id).execute()
# #                 st.success(f"Deleted '{item_title}'.")
# #                 st.rerun()
# #             except Exception as e:
# #                 st.error(f"Failed to delete content: {e}")

# # # import streamlit as st
# # # from math_saas.utils.db import get_supabase
# # # from math_saas.auth import require_admin, TEXT_MUTED


# # # def render():
# # #     """Render the Admin Content Manager panel."""
# # #     require_admin()
# # #     sb = get_supabase()

# # #     st.title("Content Manager")

# # #     # -----------------------------
# # #     # ADD NEW CONTENT
# # #     # -----------------------------
# # #     st.subheader("Add New Content")

# # #     title = st.text_input("Title")
# # #     body = st.text_area("Content", height=200)
# # #     is_premium = st.checkbox("Premium (Subscribers Only)")

# # #     if st.button("Publish"):
# # #         admin = st.session_state.get("admin")
# # #         admin_id = admin["id"] if isinstance(admin, dict) else None

# # #         if not admin_id:
# # #             st.error("Admin session invalid.")
# # #             return

# # #         try:
# # #             sb.table("public_content").insert(
# # #                 {
# # #                     "title": title.strip(),
# # #                     "body": body.strip(),
# # #                     "is_premium": is_premium,
# # #                     "created_by": admin_id,
# # #                 }
# # #             ).execute()
# # #             st.success("✅ Content published successfully.")
# # #             st.rerun()
# # #         except Exception as e:
# # #             st.error(f"Failed to publish content: {e}")

# # #     # -----------------------------
# # #     # EXISTING CONTENT
# # #     # -----------------------------
# # #     st.subheader("Existing Content")

# # #     try:
# # #         res = sb.table("public_content").select("*").order("created_at", desc=True).execute()
# # #         items_raw = res.data or []
# # #     except Exception as e:
# # #         st.error(f"Error fetching content: {e}")
# # #         return

# # #     items = [i for i in items_raw if isinstance(i, dict)]

# # #     if not items:
# # #         st.info("No content available.")
# # #         return

# # #     for item in items:
# # #         item_id = item.get("id")
# # #         item_title = item.get("title", "Untitled")
# # #         item_body = item.get("body", "")
# # #         item_premium = item.get("is_premium", False)

# # #         st.markdown(
# # #             f"""
# # #             <div class="neon-card" style="margin-bottom:16px;">
# # #                 <h4>{item_title}</h4>
# # #                 <p style="color:{TEXT_MUTED}; white-space:pre-wrap;">{item_body}</p>
# # #                 <p><strong>Premium:</strong> {item_premium}</p>
# # #             </div>
# # #             """,
# # #             unsafe_allow_html=True,
# # #         )

# # #         if item_id and st.button(f"Delete {item_title}"):
# # #             try:
# # #                 sb.table("public_content").delete().eq("id", item_id).execute()
# # #                 st.success(f"Deleted '{item_title}'.")
# # #                 st.rerun()
# # #             except Exception as e:
# # #                 st.error(f"Failed to delete content: {e}")

# # # # import streamlit as st
# # # # from math_saas.utils.db import get_supabase
# # # # from math_saas.auth import require_admin, TEXT_MUTED #noqa


# # # # def render():
# # # #     require_admin()
# # # #     sb = get_supabase()

# # # #     st.title("Content Manager")

# # # #     # -----------------------------
# # # #     # ADD NEW CONTENT
# # # #     # -----------------------------
# # # #     st.subheader("Add New Content")

# # # #     title = st.text_input("Title")
# # # #     body = st.text_area("Content", height=200)
# # # #     is_premium = st.checkbox("Premium (Subscribers Only)")

# # # #     if st.button("Publish"):
# # # #         admin = st.session_state.get("admin")
# # # #         admin_id = admin["id"] if isinstance(admin, dict) else None

# # # #         if admin_id:
# # # #             sb.table("public_content").insert(
# # # #                 {
# # # #                     "title": title,
# # # #                     "body": body,
# # # #                     "is_premium": is_premium,
# # # #                     "created_by": admin_id,
# # # #                 }
# # # #             ).execute()

# # # #             st.success("Content published.")
# # # #             st.rerun()
# # # #         else:
# # # #             st.error("Admin session invalid.")

# # # #     # -----------------------------
# # # #     # EXISTING CONTENT
# # # #     # -----------------------------
# # # #     st.subheader("Existing Content")

# # # #     res = sb.table("public_content").select("*").order("created_at", desc=True).execute()
# # # #     items_raw = res.data or []

# # # #     # Ensure items are dicts
# # # #     items = [i for i in items_raw if isinstance(i, dict)]

# # # #     if not items:
# # # #         st.info("No content available.")
# # # #         return

# # # #     for item in items:
# # # #         item_id = item.get("id")
# # # #         item_title = item.get("title", "Untitled")
# # # #         item_premium = item.get("is_premium", False)

# # # #         st.markdown(f"### {item_title}")
# # # #         st.markdown(f"**Premium:** {item_premium}")

# # # #         if item_id and st.button(f"Delete {item_id}"):
# # # #             sb.table("public_content").delete().eq("id", item_id).execute()
# # # #             st.rerun()
