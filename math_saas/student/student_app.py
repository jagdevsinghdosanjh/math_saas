import streamlit as st
from math_saas.utils.db import get_supabase

def run_student():
    st.title("Student Portal")

    supabase = get_supabase()
    res = (
        supabase.table("chapters")
        .select("title, slug, description")
        .eq("is_published", True)
        .order("created_at", asc=True)
        .execute()
    )
    chapters = res.data or []

    if not chapters:
        st.info("No chapters available yet.")
        return

    for ch in chapters:
        with st.expander(ch["title"]):
            st.write(ch.get("description") or "")
