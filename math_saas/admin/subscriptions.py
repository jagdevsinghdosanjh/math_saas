import streamlit as st
from math_saas.utils.db import get_supabase

def render():
    st.header("Subscriptions")

    sb = get_supabase()
    subs = sb.table("subscriptions").select("*").order("started_at", desc=True).execute().data

    st.dataframe(subs, width="stretch")