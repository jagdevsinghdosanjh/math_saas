import streamlit as st
from math_saas.utils.db import get_supabase
from math_saas.subscriptions.core import get_active_subscription
from math_saas.auth import TEXT_MUTED


def render_public_content():
    st.markdown("<h3>Mathematical Concepts & Latest News</h3>", unsafe_allow_html=True)

    sb = get_supabase()

    # Fetch all content
    res = sb.table("public_content").select("*").order("created_at", desc=True).execute()
    items = res.data or []

    student = st.session_state.get("student")
    user_id = student["id"] if student else None

    # Check subscription
    sub = get_active_subscription(user_id) if user_id else None
    has_access = sub is not None

    for item in items:
        premium = item.get("is_premium", False)

        # If premium and user not subscribed → show teaser only
        if premium and not has_access:
            st.markdown(
                f"""
                <div class="neon-card" style="margin-bottom:12px;">
                    <h4>{item['title']}</h4>
                    <p style="color:{TEXT_MUTED};">Premium content — subscribe to read more.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            continue

        # Full content
        st.markdown(
            f"""
            <div class="neon-card" style="margin-bottom:12px;">
                <h4>{item['title']}</h4>
                <p style="color:{TEXT_MUTED}; white-space:pre-wrap;">{item['body']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
