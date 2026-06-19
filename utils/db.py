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
# GET CLIENT
# ------------------------------------------------------------
def get_supabase() -> Client:
    return _create_client()


# ------------------------------------------------------------
# REQUIRE LOGGED-IN USER (UNIFIED MODEL)
# ------------------------------------------------------------
def require_user() -> dict:
    """
    Ensures the user is logged in using the unified auth model.
    This is the ONLY correct check across the entire app.
    """
    user = st.session_state.get("user")

    if not isinstance(user, dict):
        st.error("You are not logged in.")
        st.stop()

    return user