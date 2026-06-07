import streamlit as st
from math_saas.utils.db import get_supabase
from math_saas.auth import require_admin, TEXT_MUTED


def render():
    """Admin → Users Management Page"""
    require_admin()
    sb = get_supabase()

    st.title("Users")
    st.markdown(TEXT_MUTED("Manage all registered users."))

    # Fetch users
    try:
        res = (
            sb.table("profiles")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )
        users = res.data or []
    except Exception:
        st.error("Failed to load users. Check RLS or database connection.")
        return

    if not users:
        st.info("No users found.")
        return

    # Display table
    st.subheader("All Users")
    for u in users:
        with st.container(border=True):
            st.markdown(f"**Name:** {u.get('full_name', 'N/A')}")
            st.markdown(f"**Email:** {u.get('email', 'N/A')}")
            st.markdown(f"**Class:** {u.get('class', 'N/A')}")
            st.markdown(f"**Board:** {u.get('board', 'N/A')}")
            st.markdown(f"**Admin:** {'Yes' if u.get('is_admin') else 'No'}")
            st.markdown("---")
