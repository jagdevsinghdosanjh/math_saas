﻿import streamlit as st
from math_saas.utils.db import get_supabase

def render():
    st.header("Users")

    sb = get_supabase()
    data = sb.table("app_users").select("*").order("created_at", desc=True).execute().data

    st.subheader("All Users")
    st.dataframe(data, width="stretch")

    st.subheader("Add User")
    with st.form("add_user"):
        email = st.text_input("Email")
        name = st.text_input("Name")
        submit = st.form_submit_button("Create")

        if submit:
            sb.table("app_users").insert({"email": email, "name": name}).execute()
            st.success("User created. Refresh to see changes.")

# import streamlit as st
# from math_saas.utils.db import get_supabase

# def render():
#     st.header("Users")

#     supabase = get_supabase()
#     res = supabase.table("app_users").select("*").order("created_at", desc=True).execute()
#     users = res.data or []

#     st.subheader("All Users")
#     st.dataframe(users, width="stretch")

#     st.subheader("Add User")
#     with st.form("add_user"):
#         email = st.text_input("Email")
#         name = st.text_input("Name")
#         submitted = st.form_submit_button("Create")
#         if submitted:
#             if not email:
#                 st.error("Email is required.")
#             else:
#                 supabase.table("app_users").insert(
#                     {"email": email, "name": name}
#                 ).execute()
#                 st.success("User created. Refresh to see changes.")
