import streamlit as st
from supabase import create_client, Client
from typing import Any, Dict


# ------------------------------------------------------------
# CREATE BASE CLIENT (ANON)
# ------------------------------------------------------------
def _base_client() -> Client:
    url = st.secrets["supabase"]["url"]
    anon = st.secrets["supabase"]["anon_key"]
    return create_client(url, anon)


# ------------------------------------------------------------
# GET SUPABASE CLIENT (JWT-AWARE, v2 COMPATIBLE)
# ------------------------------------------------------------
def get_supabase() -> Client:
    client = _base_client()

    access_token = st.session_state.get("access_token")
    refresh_token = st.session_state.get("refresh_token")

    # Supabase Python v2 requires BOTH tokens as positional args
    if access_token and refresh_token:
        client.auth.set_session(access_token, refresh_token)

    return client


# ------------------------------------------------------------
# REQUIRE LOGGED-IN USER
# ------------------------------------------------------------
def require_user() -> Dict[str, Any]:
    user = st.session_state.get("user")

    if not isinstance(user, dict):
        st.error("You are not logged in.")
        st.stop()

    return user
