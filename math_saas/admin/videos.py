import streamlit as st
from typing import Any, Dict, List

from math_saas.auth import require_admin
from math_saas.utils.db import get_supabase


# ---------------------------------------------------------
# FETCH VIDEOS (TYPE-SAFE)
# ---------------------------------------------------------
def _fetch_videos() -> List[Dict[str, Any]]:
    sb = get_supabase()

    res = (
        sb.table("videos")
        .select("id, chapter_id, video_url, created_at")
        .order("created_at", desc=True)
        .execute()
    )

    raw = res.data or []
    return [row for row in raw if isinstance(row, dict)]


# ---------------------------------------------------------
# FETCH CHAPTERS FOR DROPDOWN
# ---------------------------------------------------------
def _fetch_chapters() -> List[Dict[str, Any]]:
    sb = get_supabase()

    res = (
        sb.table("chapters")
        .select("id, grade, board, chapter_key, chapter_name")
        .order("grade", desc=False)
        .execute()
    )

    raw = res.data or []
    return [row for row in raw if isinstance(row, dict)]


# ---------------------------------------------------------
# MAIN ADMIN PAGE
# ---------------------------------------------------------
def render():
    require_admin()

    st.title("Video Manager")

    # -----------------------------
    # LOAD DATA
    # -----------------------------
    videos = _fetch_videos()
    chapters = _fetch_chapters()

    # -----------------------------
    # DISPLAY EXISTING VIDEOS
    # -----------------------------
    st.subheader("All Videos")

    if not videos:
        st.info("No videos found.")
    else:
        st.dataframe(videos, width="stretch", hide_index=True)

    # -----------------------------
    # ADD NEW VIDEO
    # -----------------------------
    st.subheader("Add New Video")

    if not chapters:
        st.warning("No chapters found. Add chapters first.")
        return

    # Build chapter dropdown labels
    chapter_options = {
        f"{c['grade']} | {c['board']} | {c['chapter_key']} — {c['chapter_name']}": c["id"]
        for c in chapters
    }

    with st.form("add_video_form"):
        chapter_label = st.selectbox("Select Chapter", list(chapter_options.keys()))
        video_url = st.text_input("Video URL")

        submit = st.form_submit_button("Add Video")

        if submit:
            if not video_url:
                st.error("Video URL cannot be empty.")
                return

            chapter_id = chapter_options[chapter_label]

            sb = get_supabase()

            try:
                sb.table("videos").insert(
                    {
                        "chapter_id": chapter_id,
                        "video_url": video_url,
                    }
                ).execute()

                st.success("Video added successfully.")
                st.rerun()

            except Exception as e:
                st.error(f"Failed to add video: {e}")
