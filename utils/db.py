import streamlit as st
from supabase import create_client, Client
from typing import Optional, Any


# ------------------------------------------------------------
# CREATE CLIENT (ANON KEY ONLY)
# ------------------------------------------------------------
def _create_client() -> Client:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["anon_key"]
    return create_client(url, key)


# ------------------------------------------------------------
# GET CLIENT (NO RESTORE HERE)
# ------------------------------------------------------------
def get_supabase() -> Client:
    """
    Returns a Supabase client.
    Session restore is handled ONLY in auth.py.
    """
    return _create_client()


# ------------------------------------------------------------
# REQUIRE AUTHENTICATED USER
# ------------------------------------------------------------
def require_user(sb: Optional[Client] = None) -> Any:
    if sb is None:
        sb = get_supabase()

    res = sb.auth.get_user()
    user = res.user if res else None

    if not user:
        st.error("You are not logged in.")
        st.stop()

    return user

# from typing import Optional, Any
# from supabase import Client
# import streamlit as st
# from utils.db import get_supabase
# from supabase import create_client
# # ------------------------------------------------------------
# # CREATE CLIENT (ANON KEY ONLY)
# # ------------------------------------------------------------
# def _create_client() -> Client:
#     url = st.secrets["supabase"]["url"]
#     key = st.secrets["supabase"]["anon_key"]
#     return create_client(url, key)

# # ------------------------------------------------------------
# # GET CLIENT (NO RESTORE HERE)
# # ------------------------------------------------------------
# def get_supabase() -> Client:
#     """
#     Returns a Supabase client.
#     Session restore is handled ONLY in auth.py.
#     """
#     return _create_client()


# # ------------------------------------------------------------
# # REQUIRE AUTHENTICATED USER
# # ------------------------------------------------------------

# def require_user(sb: Optional[Client] = None) -> Any:
#     if sb is None:
#         sb = get_supabase()

#     res = sb.auth.get_user()
#     user = res.user if res else None

#     if not user:
#         st.error("You are not logged in.")
#         st.stop()

#     return user


# # import streamlit as st
# # from supabase import create_client


# # # ------------------------------------------------------------
# # # CREATE CLIENT (ANON KEY ONLY)
# # # ------------------------------------------------------------
# # def _create_client():
# #     url = st.secrets["supabase"]["url"]
# #     key = st.secrets["supabase"]["anon_key"]   # MUST be anon key
# #     return create_client(url, key)


# # # ------------------------------------------------------------
# # # RESTORE SESSION (CRITICAL)
# # # ------------------------------------------------------------
# # def restore_session(sb):
# #     """
# #     Restores Supabase session from Streamlit session_state.
# #     This is what keeps the user logged in across refreshes.
# #     """
# #     session = st.session_state.get("session")
# #     if session:
# #         access_token = session.get("access_token")
# #         if access_token:
# #             sb.auth.set_session(access_token)


# # # ------------------------------------------------------------
# # # GET CLIENT WITH RESTORED SESSION
# # # ------------------------------------------------------------
# # def get_supabase():
# #     """
# #     Returns a Supabase client with restored session.
# #     Use this everywhere in the app.
# #     """
# #     sb = _create_client()
# #     restore_session(sb)
# #     return sb


# # # ------------------------------------------------------------
# # # REQUIRE AUTHENTICATED USER
# # # ------------------------------------------------------------
# # def require_user(sb=None):
# #     """
# #     Ensures the user is logged in.
# #     If not, stops the page.
# #     """
# #     if sb is None:
# #         sb = get_supabase()

# #     user = sb.auth.get_user()
# #     if not user:
# #         st.error("You are not logged in.")
# #         st.stop()

# #     return user
