import streamlit as st
from math_saas.utils.db import supabase
import pandas as pd

def render():
    st.header("Usage Logs")

    sb = supabase()
    logs = sb.table("usage_logs").select("*").order("created_at", desc=True).limit(200).execute().data

    df = pd.DataFrame(logs)
    st.dataframe(df, use_container_width=True)

# import streamlit as st
# import pandas as pd
# from math_saas.utils.db import get_supabase

# def render():
#     st.header("Analytics")

#     supabase = get_supabase()
#     res = (
#         supabase.table("events")
#         .select("event_type, created_at")
#         .order("created_at", desc=True)
#         .limit(500)
#         .execute()
#     )
#     data = res.data or []

#     if not data:
#         st.info("No events yet.")
#         return

#     df = pd.DataFrame(data)
#     st.subheader("Recent Events")
#     st.dataframe(df, use_container_width=True)
