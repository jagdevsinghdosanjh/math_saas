import streamlit as st
from typing import Any, Dict, List

from utils.db import get_supabase
from utils.formatter import fix_math_rendering
from auth import TEXT_MUTED
from student.dashboard import get_user_active_subscription
# from utils.subscription_guard import require_active_subscription

# sub = require_active_subscription()


# ---------------------------------------------------------
# FETCH PUBLIC CONTENT (RLS‑AWARE)
# ---------------------------------------------------------
def _fetch_public_content() -> List[Dict[str, Any]]:
    sb = get_supabase()

    try:
        res = (
            sb.table("public_content")
            .select("id, title, body, category, is_premium, is_published, created_at")
            .eq("is_published", True)               # RLS + published filter
            .order("created_at", desc=True)
            .execute()
        )

        raw = res.data or []
        return [row for row in raw if isinstance(row, dict)]

    except Exception as exc:
        st.error(f"Error fetching content: {exc}")
        return []


# ---------------------------------------------------------
# MAIN RENDER FUNCTION (FINAL)
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
    sub = get_user_active_subscription(user_id) if user_id else None
    has_access = sub is not None

    # Render each content card
    for item in items:
        title = str(item.get("title", "Untitled"))
        raw_body = str(item.get("body", ""))
        body = fix_math_rendering(raw_body)

        premium = bool(item.get("is_premium", False))
        category = item.get("category", "General")

        # -------------------------------
        # PREMIUM CONTENT (LOCKED)
        # -------------------------------
        if premium and not has_access:
            st.markdown(
                f"""
                <div class="neon-card" style="margin-bottom:16px;">
                    <h4>{title}</h4>
                    <p style="color:{TEXT_MUTED}; margin-top:-8px;">
                        <em>Premium · {category}</em>
                    </p>
                    <p style="color:{TEXT_MUTED};">
                        Premium content — subscribe to read more.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            continue

        # -------------------------------
        # FULL CONTENT (FREE OR PREMIUM)
        # -------------------------------
        st.markdown(
            f"""
            <div class="neon-card" style="margin-bottom:16px;">
                <h4>{title}</h4>
                <p style="color:{TEXT_MUTED}; margin-top:-8px;">
                    <em>{"Premium" if premium else "Free"} · {category}</em>
                </p>
                <div style="color:{TEXT_MUTED}; white-space:pre-wrap;">
                    {body}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
