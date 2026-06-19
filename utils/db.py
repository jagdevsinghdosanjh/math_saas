import streamlit as st
from supabase import create_client, Client
from typing import Any, Dict


# ------------------------------------------------------------
# BASE CLIENT (ANON KEY ONLY)
# ------------------------------------------------------------
def _base_client() -> Client:
    url = st.secrets["supabase"]["url"]
    anon = st.secrets["supabase"]["anon_key"]
    return create_client(url, anon)


# ------------------------------------------------------------
# GET SUPABASE CLIENT (AUTH-AWARE)
# ------------------------------------------------------------
def get_supabase() -> Client:
    """
    Returns a Supabase client.
    If access_token + refresh_token exist, restores the authenticated session.
    Otherwise returns an anonymous client safely.
    """
    client = _base_client()

    access_token = st.session_state.get("access_token")
    refresh_token = st.session_state.get("refresh_token")

    # Only restore session if BOTH tokens exist
    if access_token and refresh_token:
        try:
            client.auth.set_session(access_token, refresh_token)
        except Exception:
            # If tokens are invalid (expired/cleared), fall back to anon client
            pass

    return client


# ------------------------------------------------------------
# REQUIRE LOGGED-IN USER (UNIFIED MODEL)
# ------------------------------------------------------------
def require_user() -> Dict[str, Any]:
    """
    Ensures the user is logged in using the unified auth model.
    Returns the user profile dict.
    """
    user = st.session_state.get("user")

    if not isinstance(user, dict):
        st.error("You are not logged in.")
        st.stop()

    return user
