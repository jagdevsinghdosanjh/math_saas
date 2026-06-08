import streamlit as st
from typing import Any, Dict, List

from math_saas.auth import require_admin
from math_saas.utils.db import get_supabase


# ---------------------------------------------------------
# FETCH ALL USERS
# ---------------------------------------------------------
def _fetch_users() -> List[Dict[str, Any]]:
    sb = get_supabase()

    res = (
        sb.table("profiles")
        .select("id, full_name, email, grade, board, is_admin, subscription_status, created_at")
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

    st.title("User Management")

    users = _fetch_users()

    if not users:
        st.info("No users found.")
        return

    # Display table
    st.subheader("All Users")
    st.dataframe(users, use_container_width=True, hide_index=True)

    # Inspect user
    st.subheader("Inspect User")

    ids = [str(u["id"]) for u in users]
    selected_id = st.selectbox("Select User ID", ids, key="admin_user_select")

    selected = next((u for u in users if str(u["id"]) == selected_id), None)

    if selected:
        st.json(selected)

    # Admin-only user creation
    st.subheader("Add New User (Admin Only)")

    with st.form("add_user_form"):
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        grade = st.text_input("Grade (optional)")
        board = st.text_input("Board (optional)")
        is_admin = st.checkbox("Is Admin?", value=False)

        submit = st.form_submit_button("Create User")

        if submit:
            sb = get_supabase()

            try:
                sb.table("profiles").insert(
                    {
                        "full_name": full_name,
                        "email": email,
                        "grade": grade or None,
                        "board": board or None,
                        "is_admin": is_admin,
                        "subscription_status": "free",
                    }
                ).execute()

                st.success("User created successfully.")
                st.rerun()

            except Exception as e:
                st.error(f"Failed to create user: {e}")
