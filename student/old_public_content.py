import streamlit as st
from typing import Any, Dict, List

from utils.db import get_supabase
from utils.formatter import fix_math_rendering
from auth import TEXT_MUTED
from student.dashboard import get_user_active_subscription

# from math_saas.subscriptions.core import get_active_subscription


# ---------------------------------------------------------
# FETCH PUBLIC CONTENT (TYPE-SAFE)
# ---------------------------------------------------------
def _fetch_public_content() -> List[Dict[str, Any]]:
    sb = get_supabase()

    try:
        res = (
            sb.table("public_content")
            .select("id, title, body, is_premium, created_at")
            .order("created_at", desc=True)
            .execute()
        )
        raw = res.data or []
        return [row for row in raw if isinstance(row, dict)]

    except Exception as exc:
        st.error(f"Error fetching content: {exc}")
        return []


# ---------------------------------------------------------
# MAIN RENDER FUNCTION
# ---------------------------------------------------------
def render_public_content():
    st.markdown("<h3>Mathematical Concepts & Latest News</h3>", unsafe_allow_html=True)

    items = _fetch_public_content()
    if not items:
        st.info("No public content available.")
        return

    # Student session
    student = st.session_state.get("student")
    user_id = student.get("id") if isinstance(student, dict) else None

    # Subscription check
# Subscription check (NEW)
    sub = get_user_active_subscription(user_id) if user_id else None
    has_access = sub is not None


    # Render each content card
    for item in items:
        title = str(item.get("title", "Untitled"))
        raw_body = str(item.get("body", ""))
        body = fix_math_rendering(raw_body)
        premium = bool(item.get("is_premium", False))

        # Premium content but user not subscribed → teaser only
        if premium and not has_access:
            st.markdown(
                f"""
                <div class="neon-card" style="margin-bottom:16px;">
                    <h4>{title}</h4>
                    <p style="color:{TEXT_MUTED};">
                        Premium content — subscribe to read more.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            continue

        # Full content
        st.markdown(
            f"""
            <div class="neon-card" style="margin-bottom:16px;">
                <h4>{title}</h4>
                <div style="color:{TEXT_MUTED}; white-space:pre-wrap;">
                    {body}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
