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


# GET SUPABASE CLIENT (AUTH-AWARE)
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


# REQUIRE LOGGED-IN USER (UNIFIED MODEL)
def require_user() -> Dict[str, Any]:
    """
    Ensures the user is logged in.
    Accepts both dict (profiles table) and Supabase User objects.
    Returns a normalized dict.
    """
    user = st.session_state.get("user")

    # Case 1: dict from login handler
    if isinstance(user, dict):
        return user

    # Case 2: Supabase User object (Pydantic)
    if user is not None:
        meta = getattr(user, "user_metadata", {}) or {}
        email = getattr(user, "email", None)

        return {
            "id": getattr(user, "id", None),
            "email": email,
            "full_name": meta.get("full_name"),
            "name": meta.get("name"),
            "is_admin": meta.get("is_admin", False),
        }

    # Case 3: no user at all
    st.error("You are not logged in.")
    st.stop()