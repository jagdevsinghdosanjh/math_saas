import streamlit as st
from typing import Any, Dict, List

from math_saas.utils.db import get_supabase
from math_saas.auth import TEXT_MUTED
from math_saas.subscriptions.core import get_active_subscription


# ---------------------------------------------------------
# FETCH CHAPTERS (TYPE-SAFE)
# ---------------------------------------------------------
def _fetch_chapters() -> List[Dict[str, Any]]:
    sb = get_supabase()

    try:
        res = (
            sb.table("chapters")
            .select("id, title, description, order_index, is_premium")
            .order("order_index", desc=False)  # ASCENDING ORDER
            .execute()
        )
        raw = res.data or []
        return [row for row in raw if isinstance(row, dict)]
    except Exception as exc:
        st.error(f"Error loading chapters: {exc}")
        return []


# ---------------------------------------------------------
# FETCH PROGRESS (TYPE-SAFE)
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
            if isinstance(row, dict):
                cid = str(row.get("chapter_id", ""))
                prog_raw = row.get("progress", 0)

                # Safe float conversion
                if isinstance(prog_raw, (int, float)):
                    progress_map[cid] = float(prog_raw)
                else:
                    try:
                        progress_map[cid] = float(str(prog_raw))
                    except Exception:
                        progress_map[cid] = 0.0

        return progress_map

    except Exception:
        return {}


# ---------------------------------------------------------
# MAIN RENDER FUNCTION
# ---------------------------------------------------------
def render_chapters_page() -> None:
    st.markdown("<h3>Chapters</h3>", unsafe_allow_html=True)

    # Validate student session
    student = st.session_state.get("student")
    if not isinstance(student, dict):
        st.error("Please login as student.")
        return

    raw_id = student.get("id")
    user_id = str(raw_id) if raw_id is not None else ""

    if not user_id:
        st.error("Invalid student session.")
        return

    # Subscription check
    active_sub = get_active_subscription(user_id)
    has_premium = active_sub is not None

    # Fetch chapters + progress
    chapters = _fetch_chapters()
    progress_map = _fetch_progress(user_id)

    if not chapters:
        st.info("No chapters available yet.")
        return

    # Render each chapter card
    for ch in chapters:
        cid = str(ch.get("id", ""))
        title = str(ch.get("title", "Untitled"))
        desc = str(ch.get("description", ""))
        premium = bool(ch.get("is_premium", False))

        # Safe progress extraction
        prog_raw = progress_map.get(cid, 0)

        if isinstance(prog_raw, (int, float)):
            progress = float(prog_raw)
        else:
            try:
                progress = float(str(prog_raw))
            except Exception:
                progress = 0.0

        locked = premium and not has_premium

        # Card UI
        st.markdown(
            f"""
            <div class="neon-card" style="margin-bottom:16px;">
                <h4 style="margin:0;">{title}</h4>
                <p style="color:{TEXT_MUTED}; margin:4px 0 8px 0;">
                    {desc}
                </p>
                <p style="color:{TEXT_MUTED}; margin:0;">
                    {'Premium Chapter 🔒' if locked else 'Accessible ✔️'}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Progress bar (always receives a valid float)
        st.progress(progress)

        # Action button
        if locked:
            st.button("Unlock with Subscription", key=f"unlock_{cid}", disabled=True)
        else:
            if st.button("Open Chapter", key=f"open_{cid}"):
                st.session_state["chapter_id"] = cid
                st.session_state["page"] = "chapter_detail"
                st.rerun()

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
