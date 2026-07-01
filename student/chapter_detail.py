import streamlit as st
from utils.db import get_supabase
from typing import List, Dict, Any, cast

def render_chapter_detail():
    sb = get_supabase()

    # Ensure chapter_id is int
    chapter_id = int(st.session_state.get("chapter_id") or 0)
    if chapter_id == 0:
        st.error("No chapter selected.")
        return

    # Fetch chapter info
    chapter_res = (
        sb.table("chapters")
        .select("*")
        .eq("id", chapter_id)
        .single()
        .execute()
    )

    chapter = cast(Dict[str, Any], chapter_res.data or {})
    chapter_name = chapter.get("chapter_name", "Untitled")

    st.markdown(f"## {chapter_name}")

    # Fetch PDFs
    pdf_res = (
        sb.table("pdf_notes")
        .select("*")
        .eq("chapter_id", chapter_id)
        .order("id")
        .execute()
    )
    pdfs: List[Dict[str, Any]] = cast(List[Dict[str, Any]], pdf_res.data or [])

    # Fetch Videos
    video_res = (
        sb.table("videos")
        .select("*")
        .eq("chapter_id", chapter_id)
        .order("id")
        .execute()
    )
    videos: List[Dict[str, Any]] = cast(List[Dict[str, Any]], video_res.data or [])

    # Render PDFs
    if pdfs:
        st.markdown("### 📄 PDF Notes")
        for pdf in pdfs:
            url = str(pdf.get("pdf_url", ""))
            st.markdown(f"- [Open PDF]({url})")

    # Render Videos
    if videos:
        st.markdown("### 🎥 Videos")
        for vid in videos:
            url = str(vid.get("video_url", ""))
            st.video(url)

    if not pdfs and not videos:
        st.info("No content available for this chapter.")

    if st.button("⬅ Back"):
        st.session_state["chapter_mode"] = "list"
        st.rerun()
