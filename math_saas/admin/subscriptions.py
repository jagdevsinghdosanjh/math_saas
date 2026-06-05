import streamlit as st
from math_saas.utils.db import supabase

def render():
    st.header("Subscriptions")

    sb = supabase()
    subs = sb.table("subscriptions").select("*").order("started_at", desc=True).execute().data

    st.dataframe(subs, use_container_width=True)

# import streamlit as st
# from math_saas.utils.db import get_supabase

# def render():
#     st.header("Subscriptions")

#     supabase = get_supabase()
#     res = (
#         supabase.table("subscriptions")
#         .select("id, plan, status, started_at, ends_at, user_id")
#         .order("started_at", desc=True)
#         .execute()
#     )
#     subs = res.data or []

#     st.subheader("All Subscriptions")
#     st.dataframe(subs, use_container_width=True)
