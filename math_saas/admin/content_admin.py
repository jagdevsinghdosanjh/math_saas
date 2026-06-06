import streamlit as st
from math_saas.utils.db import get_supabase
from math_saas.auth import require_admin


def render():
    require_admin()
    sb = get_supabase()

    st.title("Content Manager")

    st.subheader("Add New Content")

    title = st.text_input("Title")
    body = st.text_area("Content", height=200)
    is_premium = st.checkbox("Premium (Subscribers Only)")

    if st.button("Publish"):
        admin = st.session_state["admin"]
        sb.table("public_content").insert(
            {
                "title": title,
                "body": body,
                "is_premium": is_premium,
                "created_by": admin["id"],
            }
        ).execute()
        st.success("Content published.")
        st.rerun()

    st.subheader("Existing Content")

    res = sb.table("public_content").select("*").order("created_at", desc=True).execute()
    items = res.data or []

    for item in items:
        st.markdown(f"### {item['title']}")
        st.markdown(f"Premium: {item['is_premium']}")
        if st.button(f"Delete {item['id']}"):
            sb.table("public_content").delete().eq("id", item["id"]).execute()
            st.rerun()
