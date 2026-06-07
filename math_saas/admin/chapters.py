import streamlit as st
from math_saas.utils.db import get_supabase

def render():
    st.header("Chapters")

    sb = get_supabase()
    chapters = sb.table("chapters").select("*").order("id", desc=True).execute().data

    st.subheader("All Chapters")
    st.dataframe(chapters, width="stretch")

    st.subheader("Add Chapter")
    with st.form("add_chapter"):
        grade = st.text_input("Grade")
        board = st.text_input("Board")
        chapter_key = st.text_input("Chapter Key")
        chapter_name = st.text_input("Chapter Name")
        submit = st.form_submit_button("Create")

        if submit:
            sb.table("chapters").insert({
                "grade": grade,
                "board": board,
                "chapter_key": chapter_key,
                "chapter_name": chapter_name
            }).execute()
            st.success("Chapter added. Refresh to see changes.")
