import streamlit as st
from math_saas.utils.db import get_supabase

def render():
    st.header("Settings")

    sb = get_supabase()
    settings = sb.table("settings").select("*").execute().data

    st.dataframe(settings, width="stretch")

    st.subheader("Update Setting")
    with st.form("update_setting"):
        key = st.text_input("Key")
        value = st.text_input("Value")
        submit = st.form_submit_button("Save")

        if submit:
            sb.table("settings").upsert({"key": key, "value": value}).execute()
            st.success("Setting saved.")
