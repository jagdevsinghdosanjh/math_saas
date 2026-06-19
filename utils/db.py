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