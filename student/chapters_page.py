import streamlit as st
from typing import Any, Dict, List

from utils.db import get_supabase
from auth import TEXT_MUTED
from student.dashboard import get_user_active_subscription


# ---------------------------------------------------------
# SAFE FLOAT CONVERSION
# ---------------------------------------------------------
def safe_float(value: Any) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0


# ---------------------------------------------------------
# FETCH CHAPTERS (Typed + Clean)
# ---------------------------------------------------------
def fetch_chapters(grade: str, board: str) -> List[Dict[str, Any]]:
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

        data = res.data or []
        return [row for row in data if isinstance(row, dict)]

    except Exception as exc:
        st.error(f"Error loading chapters: {exc}")
        return []


# ---------------------------------------------------------
# FETCH PROGRESS (Typed + Clean)
# ---------------------------------------------------------
def fetch_progress(user_id: str) -> Dict[str, float]:
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
            if isinstance(row, dict):
                cid = str(row.get("chapter_id", ""))
                progress_map[cid] = safe_float(row.get("progress", 0))

        return progress_map

    except Exception:
        return {}


# ---------------------------------------------------------
# CHAPTER CARD COMPONENT
# ---------------------------------------------------------
def render_chapter_card(
    chapter: Dict[str, Any],
    progress: float,
    locked: bool
) -> None:

    cid = str(chapter.get("id", ""))
    chapter_name = str(chapter.get("chapter_name", "Untitled"))
    chapter_key = str(chapter.get("chapter_key", ""))

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


# ---------------------------------------------------------
# MAIN RENDER FUNCTION (FINAL, CLEAN)
# ---------------------------------------------------------
def render_chapters_page(sb=None, user=None) -> None:
    st.markdown("<h3>Chapters</h3>", unsafe_allow_html=True)

    # Restore Supabase session
    if sb is None:
        sb = get_supabase()

    res = sb.auth.get_user()
    user = res.user if res else None

    if not user:
        st.error("You are not logged in.")
        st.stop()

    user_id = user.id

    # Fetch grade + board
    profile_res = (
        sb.table("profiles")
        .select("grade, board")
        .eq("id", user_id)
        .single()
        .execute()
    )

    profile = profile_res.data or {}
    grade = str(profile.get("grade") or "")
    board = str(profile.get("board") or "")

    if not grade or not board:
        st.error("Your profile is incomplete. Please update grade/board.")
        return

    # Subscription check
    active_sub = get_user_active_subscription(user_id)
    has_premium = active_sub is not None

    # Fetch chapters + progress
    chapters = fetch_chapters(grade, board)
    progress_map = fetch_progress(user_id)

    if not isinstance(progress_map, dict):
        progress_map = {}

    if not chapters:
        st.info("No chapters available for your grade/board.")
        return 
    
    # Render chapter cards
    for chapter in chapters:
        cid = str(chapter.get("id", ""))
        chapter_key = str(chapter.get("chapter_key", ""))
        premium = chapter_key.lower().startswith("p_")
        locked = premium and not has_premium
        progress = safe_float(progress_map.get(cid, 0))
        render_chapter_card(chapter, progress, locked)