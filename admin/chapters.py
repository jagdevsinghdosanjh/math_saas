import streamlit as st
from typing import Any, Dict, List
from auth import require_admin
from utils.db import get_supabase_admin

# ---------------------------------------------------------
# FETCH CHAPTERS (TYPE-SAFE)
# ---------------------------------------------------------
def _fetch_chapters() -> List[Dict[str, Any]]:
    sb = get_supabase_admin()

    res = (
        sb.table("chapters")
        .select("id, grade, board, chapter_key, chapter_name, created_at")
        .order("id", desc=False)
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

    # Show persistent success message after rerun
    if st.session_state.get("delete_success"):
        st.success(st.session_state["delete_success"])
        st.session_state["delete_success"] = None

    sb = get_supabase_admin()
    chapters = _fetch_chapters()

    st.subheader("All Chapters")

    if not chapters:
        st.info("No chapters found.")
    else:
        for ch in chapters:
            cid = ch["id"]
            grade = ch["grade"]
            board = ch["board"]
            key = ch["chapter_key"]
            name = ch["chapter_name"]
            created = ch["created_at"]

            with st.container():
                st.markdown(
                    f"""
                    <div class="neon-card" style="padding:14px; margin-bottom:12px;">
                        <h4 style="margin:0;">{name}</h4>
                        <p style="margin:0; color:#9ca3af;">
                            Grade: {grade} | Board: {board} | Key: {key}
                        </p>
                        <p style="margin:0; color:#6b7280; font-size:0.8rem;">
                            Created: {created}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # STEP 1 — Delete button clicked
                if st.button(f"Delete Chapter {cid}", key=f"del_{cid}"):
                    st.session_state["confirm_delete"] = cid

                # STEP 2 — Show warning + confirm button ONLY for selected chapter
                if st.session_state.get("confirm_delete") == cid:
                    st.error(
                        f"⚠️ WARNING: Deleting chapter {cid} will remove:\n"
                        "- All PDF notes\n"
                        "- All videos\n"
                        "- All student progress\n"
                        "- The chapter itself\n\n"
                        "This action cannot be undone."
                    )
                    if st.button(f"Confirm Delete {cid}", key=f"confirm_del_{cid}"):
                        try:
                            sb.table("pdf_notes").delete().eq("chapter_id", cid).execute()
                            sb.table("videos").delete().eq("chapter_id", cid).execute()
                            sb.table("chapter_progress").delete().eq("chapter_id", cid).execute()
                            sb.table("chapters").delete().eq("id", cid).execute()

                            # Persist success message across rerun
                            st.session_state["delete_success"] = (
                                f"Chapter {cid} deleted successfully."
                            )

                            # Clear delete flag
                            st.session_state["confirm_delete"] = None
                            st.rerun()

                        except Exception as exc:
                            st.error(f"Failed to delete chapter: {exc}")
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
