import streamlit as st
from typing import Any, Dict, List

from math_saas.auth import require_admin
from math_saas.utils.db import get_supabase


# ---------------------------------------------------------
# FETCH CHAPTERS (TYPE-SAFE)
# ---------------------------------------------------------
def _fetch_chapters() -> List[Dict[str, Any]]:
    sb = get_supabase()

    res = (
        sb.table("chapters")
        .select("id, grade, board, chapter_key, chapter_name, created_at")
        .order("created_at", desc=True)
        .execute()
    )

    raw = res.data or []
    return [row for row in raw if isinstance(row, dict)]


# ---------------------------------------------------------
# MAIN ADMIN PAGE
# ---------------------------------------------------------
def render():
    require_admin()

    st.title("Chapters Management")

    chapters = _fetch_chapters()

    # -----------------------------
    # DISPLAY TABLE
    # -----------------------------
    st.subheader("All Chapters")

    if not chapters:
        st.info("No chapters found.")
    else:
        st.dataframe(chapters, width="stretch", hide_index=True)

    # -----------------------------
    # ADD NEW CHAPTER
    # -----------------------------
    st.subheader("Add New Chapter")

    with st.form("add_chapter_form"):
        grade = st.text_input("Grade (e.g., 9, 10)")
        board = st.text_input("Board (e.g., CBSE, PSEB)")
        chapter_key = st.text_input("Chapter Key (unique identifier)")
        chapter_name = st.text_input("Chapter Name")

        submit = st.form_submit_button("Create Chapter")

        if submit:
            if not grade or not board or not chapter_key or not chapter_name:
                st.error("All fields are required.")
                return

            sb = get_supabase()

            # Prevent duplicate chapter_key for same grade+board
            existing = (
                sb.table("chapters")
                .select("id")
                .eq("grade", grade)
                .eq("board", board)
                .eq("chapter_key", chapter_key)
                .execute()
                .data
            )

            if existing:
                st.error("A chapter with this key already exists for this grade and board.")
                return

            try:
                sb.table("chapters").insert(
                    {
                        "grade": grade,
                        "board": board,
                        "chapter_key": chapter_key,
                        "chapter_name": chapter_name,
                    }
                ).execute()

                st.success("Chapter added successfully.")
                st.rerun()

            except Exception as e:
                st.error(f"Failed to add chapter: {e}")
