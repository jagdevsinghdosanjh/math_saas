import streamlit as st
from typing import Any, Dict, List

from auth import require_admin
from utils.db import get_supabase
from admin.delete_user import delete_user


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
# MAIN ADMIN PAGE (ONLY ONE RENDER FUNCTION)
# ---------------------------------------------------------
def render():
    require_admin()

    st.title("👥 User Management")

    users = _fetch_users()

    if not users:
        st.info("No users found.")
        return

    # ---------------------------------------------------------
    # USERS TABLE
    # ---------------------------------------------------------
    st.subheader("All Users")
    st.dataframe(users, width="stretch", hide_index=True)

    # ---------------------------------------------------------
    # INSPECT USER
    # ---------------------------------------------------------
    st.subheader("Inspect User")

    ids = [str(u["id"]) for u in users]
    selected_id = st.selectbox("Select User ID", ids, key="admin_user_select")

    selected = next((u for u in users if str(u["id"]) == selected_id), None)

    if selected:
        st.json(selected)

        # ---------------------------------------------------------
        # DELETE USER (EXCEPT ADMINS)
        # ---------------------------------------------------------
        if not selected.get("is_admin", False):
            if st.button("Delete This User", key=f"delete_{selected_id}"):
                ok = delete_user(selected_id)
                if ok:
                    st.success("User deleted successfully.")
                    st.rerun()
        else:
            st.info("Admin accounts cannot be deleted.")

    # ---------------------------------------------------------
    # CREATE NEW USER
    # ---------------------------------------------------------
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

# import streamlit as st
# from typing import Any, Dict, List

# from auth import require_admin
# from utils.db import get_supabase

# from admin.delete_user import delete_user
# import streamlit as st

# # -------------------------------------------------
# # USERS PAGE (ADMIN)
# # -------------------------------------------------
# def render():
#     st.title("👥 Manage Users")

#     sb = get_supabase()

#     # Fetch all users from profiles table
#     res = sb.table("profiles").select("*").execute()
#     users = res.data or []

#     if not isinstance(users, list):
#         st.error("Invalid data received from Supabase.")
#         return

#     if len(users) == 0:
#         st.info("No users found.")
#         return

#     # Display each user
#     for user in users:
#         if not isinstance(user, dict):
#             continue  # skip invalid rows

#         uid_raw = user.get("id")
#         uid = str(uid_raw) if uid_raw is not None else None

#         email = user.get("email")
#         name = user.get("full_name") or user.get("name") or "Unnamed User"
#         is_admin = user.get("is_admin", False)

#         with st.container():
#             st.markdown(f"### {name}")
#             st.write(f"📧 Email: {email}")
#             st.write(f"🆔 User ID: `{uid}`")
#             st.write(f"🔐 Admin: {'Yes' if is_admin else 'No'}")

#             # Delete button
#             if not is_admin:  # Prevent deleting admin accounts
#                 if st.button("Delete User", key=f"del_{uid}"):
#                     if uid is None:
#                         st.error("Invalid user ID.")
#                         continue

#                     ok = delete_user(uid)
#                     if ok:
#                         st.success(f"User {name} deleted successfully.")
#                         st.rerun()
#             else:
#                 st.info("Admin accounts cannot be deleted.")


# # ---------------------------------------------------------
# # FETCH ALL USERS
# # ---------------------------------------------------------
# def _fetch_users() -> List[Dict[str, Any]]:
#     sb = get_supabase()

#     res = (
#         sb.table("profiles")
#         .select("id, full_name, email, grade, board, is_admin, subscription_status, created_at")
#         .order("created_at", desc=True)
#         .execute()
#     )

#     raw = res.data or []
#     return [row for row in raw if isinstance(row, dict)]


# # ---------------------------------------------------------
# # MAIN ADMIN PAGE
# # ---------------------------------------------------------
# def render():
#     require_admin()

#     st.title("User Management")

#     users = _fetch_users()

#     if not users:
#         st.info("No users found.")
#         return

#     # Display table
#     st.subheader("All Users")
#     st.dataframe(users, width="stretch", hide_index=True)

#     # Inspect user
#     st.subheader("Inspect User")

#     ids = [str(u["id"]) for u in users]
#     selected_id = st.selectbox("Select User ID", ids, key="admin_user_select")

#     selected = next((u for u in users if str(u["id"]) == selected_id), None)

#     if selected:
#         st.json(selected)

#     # Admin-only user creation
#     st.subheader("Add New User (Admin Only)")

#     with st.form("add_user_form"):
#         full_name = st.text_input("Full Name")
#         email = st.text_input("Email")
#         grade = st.text_input("Grade (optional)")
#         board = st.text_input("Board (optional)")
#         is_admin = st.checkbox("Is Admin?", value=False)

#         submit = st.form_submit_button("Create User")

#         if submit:
#             sb = get_supabase()

#             try:
#                 sb.table("profiles").insert(
#                     {
#                         "full_name": full_name,
#                         "email": email,
#                         "grade": grade or None,
#                         "board": board or None,
#                         "is_admin": is_admin,
#                         "subscription_status": "free",
#                     }
#                 ).execute()

#                 st.success("User created successfully.")
#                 st.rerun()

#             except Exception as e:
#                 st.error(f"Failed to create user: {e}")
