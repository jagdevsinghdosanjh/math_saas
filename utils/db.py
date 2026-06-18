import streamlit as st
from supabase import create_client, Client
from typing import Optional, Any


def _create_client() -> Client:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["anon_key"]
    return create_client(url, key)


def get_supabase() -> Client:
    return _create_client()

def require_user() -> dict:
    user = st.session_state.get("user")

    if not isinstance(user, dict):
        st.error("You are not logged in.")
        st.stop()

    return user

# def require_user(sb: Optional[Client] = None) -> Any:
#     """
#     Trust the unified Streamlit session model instead of sb.auth.get_user().
#     """
#     user = st.session_state.get("user")

#     if not isinstance(user, dict):
#         st.error("You are not logged in.")
#         st.stop()

#     return user

# import streamlit as st
# from supabase import create_client, Client
# from typing import Optional, Any

# def _create_client() -> Client:
#     url = st.secrets["supabase"]["url"]
#     key = st.secrets["supabase"]["anon_key"]
#     return create_client(url, key)

# def get_supabase() -> Client:
#     return _create_client()

# def require_user(sb: Optional[Client] = None) -> Any:
#     if sb is None:
#         sb = get_supabase()

#     res = sb.auth.get_user()
#     user = res.user if res else None

#     if not user:
#         st.error("You are not logged in.")
#         st.stop()

#     return user
