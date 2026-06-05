import streamlit as st
from math_saas.utils.db import supabase

def render():
    st.header("Videos")

    sb = supabase()
    videos = sb.table("videos").select("*").order("id", desc=True).execute().data

    st.dataframe(videos, use_container_width=True)

    st.subheader("Add Video")
    with st.form("add_video"):
        chapter_id = st.number_input("Chapter ID", step=1)
        video_url = st.text_input("Video URL")
        submit = st.form_submit_button("Create")

        if submit:
            sb.table("videos").insert({
                "chapter_id": chapter_id,
                "video_url": video_url
            }).execute()
            st.success("Video added.")
