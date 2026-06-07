import streamlit as st
from utils.db import get_supabase

def render():
    st.header("PDF Notes")

    sb = get_supabase()
    notes = sb.table("pdf_notes").select("*").order("id", desc=True).execute().data

    st.dataframe(notes, width="stretch")

    st.subheader("Add PDF Note")
    with st.form("add_pdf"):
        chapter_id = st.number_input("Chapter ID", step=1)
        pdf_url = st.text_input("PDF URL")
        submit = st.form_submit_button("Create")

        if submit:
            sb.table("pdf_notes").insert({
                "chapter_id": chapter_id,
                "pdf_url": pdf_url
            }).execute()
            st.success("PDF added.")
