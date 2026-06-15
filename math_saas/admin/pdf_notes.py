import streamlit as st
from typing import Any, Dict, List

from math_saas.auth import require_admin
from math_saas.utils.db import get_supabase


# ---------------------------------------------------------
# FETCH PDF NOTES (TYPE-SAFE)
# ---------------------------------------------------------
def _fetch_pdf_notes() -> List[Dict[str, Any]]:
    sb = get_supabase()

    res = (
        sb.table("pdf_notes")
        .select("id, chapter_id, pdf_url, created_at")
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

    st.title("PDF Notes Manager")

    # -----------------------------
    # LOAD DATA
    # -----------------------------
    notes = _fetch_pdf_notes()
    chapters = _fetch_chapters()

    # -----------------------------
    # DISPLAY EXISTING PDF NOTES
    # -----------------------------
    st.subheader("All PDF Notes")

    if not notes:
        st.info("No PDF notes found.")
    else:
        st.dataframe(notes, width="stretch", hide_index=True)

    # -----------------------------
    # ADD NEW PDF NOTE
    # -----------------------------
    st.subheader("Add New PDF Note")

    if not chapters:
        st.warning("No chapters found. Add chapters first.")
        return

    # Build chapter dropdown labels
    chapter_options = {
        f"{c['grade']} | {c['board']} | {c['chapter_key']} — {c['chapter_name']}": c["id"]
        for c in chapters
    }

    with st.form("add_pdf_form"):
        chapter_label = st.selectbox("Select Chapter", list(chapter_options.keys()))
        pdf_url = st.text_input("PDF URL")

        submit = st.form_submit_button("Add PDF Note")

        if submit:
            if not pdf_url:
                st.error("PDF URL cannot be empty.")
                return

            chapter_id = chapter_options[chapter_label]

            sb = get_supabase()

            try:
                sb.table("pdf_notes").insert(
                    {
                        "chapter_id": chapter_id,
                        "pdf_url": pdf_url,
                    }
                ).execute()

                st.success("PDF note added successfully.")
                st.rerun()

            except Exception as e:
                st.error(f"Failed to add PDF note: {e}")
