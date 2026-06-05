import streamlit as st
from typing import Optional, TypedDict, cast
from math_saas.utils.db import supabase


class Profile(TypedDict, total=False):
    id: str
    email: str
    is_admin: bool


def _login_form():
    st.subheader("Admin Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login", type="primary"):
        sb = supabase()

        try:
            res = sb.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
        except Exception:
            st.error("Invalid login credentials")
            return

        user = res.user
        if not user:
            st.error("Invalid login credentials")
            return

        # Fetch profile
        result = (
            sb.table("profiles")
            .select("id, email, is_admin")
            .eq("id", user.id)
            .single()
            .execute()
        )

        # Cast JSON → Profile | None (fixes Pylance)
        profile = cast(Optional[Profile], result.data)

        if not profile:
            st.error("Profile not found in database")
            return

        if not profile.get("is_admin"):
            st.error("You are not authorized as admin")
            return

        st.session_state["user"] = profile
        st.session_state["is_admin"] = True
        st.success("Logged in successfully")
        st.rerun()

def require_admin():
    if st.session_state.get("is_admin"):
        return
    _login_form()
    st.stop()

# import streamlit as st
# from typing import Optional, TypedDict
# from math_saas.utils.db import supabase


# class Profile(TypedDict, total=False):
#     id: str
#     email: str
#     is_admin: bool


# def _login_form():
#     st.subheader("Admin Login")
#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")

#     if st.button("Login", type="primary"):
#         sb = supabase()

#         try:
#             res = sb.auth.sign_in_with_password(
#                 {"email": email, "password": password}
#             )
#         except Exception:
#             st.error("Invalid login credentials")
#             return

#         user = res.user
#         if not user:
#             st.error("Invalid login credentials")
#             return

#         # Fetch profile (now typed correctly)
#         result = (
#             sb.table("profiles")
#             .select("id, email, is_admin")
#             .eq("id", user.id)
#             .single()
#             .execute()
#         )

#         profile: Optional[Profile] = result.data  # <-- FIXED

#         if not profile:
#             st.error("Profile not found in database")
#             return

#         if not profile.get("is_admin"):
#             st.error("You are not authorized as admin")
#             return

#         st.session_state["user"] = profile
#         st.session_state["is_admin"] = True
#         st.success("Logged in successfully")


# def require_admin():
#     if st.session_state.get("is_admin"):
#         return
#     _login_form()
#     st.stop()
