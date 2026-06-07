﻿import streamlit as st
from math_saas.utils.db import get_supabase
import pandas as pd
def render():
    st.header("Usage Logs")

    sb = get_supabase()
    logs = sb.table("usage_logs").select("*").order("created_at", desc=True).limit(200).execute().data

    df = pd.DataFrame(logs)
    st.dataframe(df, width="stretch")