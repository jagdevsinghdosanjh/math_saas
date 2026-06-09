import streamlit as st
from typing import Any, Dict, List

from math_saas.utils.db import get_supabase
from math_saas.auth import TEXT_MUTED
from math_saas.subscriptions.core import get_active_subscription


# ---------------------------------------------------------
# SAFE FLOAT CONVERSION (Pylance-clean)
# ---------------------------------------------------------
def safe_float(value: Any) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0


# ---------------------------------------------------------
# FETCH CHAPTERS
# ---------------------------------------------------------
def _fetch_chapters(grade: str, board: str) -> List[Dict[str, Any]]:
    sb = get_supabase()

    try:
        res = (
            sb.table("chapters")
            .select("id, grade, board, chapter_key, chapter_name, created_at")
            .eq("grade", grade)
            .eq("board", board)
            .order("id", desc=False)
            .execute()
        )

        raw = res.data or []
        return [row for row in raw if isinstance(row, dict)]

    except Exception as exc:
        st.error(f"Error loading chapters: {exc}")
        return []


# ---------------------------------------------------------
# FETCH PROGRESS
# ---------------------------------------------------------
def _fetch_progress(user_id: str) -> Dict[str, float]:
    sb = get_supabase()

    try:
        res = (
            sb.table("chapter_progress")
            .select("chapter_id, progress")
            .eq("user_id", user_id)
            .execute()
        )

        raw = res.data or []
        progress_map: Dict[str, float] = {}

        for row in raw:
            if not isinstance(row, dict):
                continue

            cid = str(row.get("chapter_id", ""))
            progress_map[cid] = safe_float(row.get("progress", 0))

        return progress_map

    except Exception:
        return {}


# ---------------------------------------------------------
# MAIN RENDER FUNCTION
# ---------------------------------------------------------
def render_chapters_page() -> None:
    st.markdown("<h3>Chapters</h3>", unsafe_allow_html=True)

    student = st.session_state.get("student")
    if not isinstance(student, dict):
        st.error("Please login as student.")
        return

    user_id = str(student.get("id") or "")
    grade = str(student.get("grade") or "")
    board = str(student.get("board") or "")

    if not user_id or not grade or not board:
        st.error("Invalid student session.")
        return

    active_sub = get_active_subscription(user_id)
    has_premium = active_sub is not None

    chapters = _fetch_chapters(grade, board)
    progress_map = _fetch_progress(user_id)

    if not chapters:
        st.info("No chapters available for your grade/board.")
        return

    for ch in chapters:
        cid = str(ch.get("id", ""))
        chapter_name = str(ch.get("chapter_name", "Untitled"))
        chapter_key = str(ch.get("chapter_key", ""))

        premium = chapter_key.lower().startswith("p_")
        locked = premium and not has_premium

        # Pylance-clean float
        progress = safe_float(progress_map.get(cid, 0))

        st.markdown(
            f"""
            <div class="neon-card" style="margin-bottom:16px;">
                <h4 style="margin:0;">{chapter_name}</h4>
                <p style="color:{TEXT_MUTED}; margin:4px 0 8px 0;">
                    Key: {chapter_key}
                </p>
                <p style="color:{TEXT_MUTED}; margin:0;">
                    {'Premium Chapter 🔒' if locked else 'Accessible ✔️'}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.progress(progress)

        if locked:
            st.button("Unlock with Subscription", key=f"unlock_{cid}", disabled=True)
        else:
            if st.button("Open Chapter", key=f"open_{cid}"):
                st.session_state["chapter_id"] = cid
                st.session_state["page"] = "chapter_detail"
                st.rerun()

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
