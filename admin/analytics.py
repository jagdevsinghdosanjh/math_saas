import streamlit as st
import pandas as pd
from typing import Any, Dict, List, Optional

from auth import require_admin
from utils.db import get_supabase


# ---------------------------------------------------------
# FETCH LOGS (TYPE-SAFE)
# ---------------------------------------------------------
def _fetch_logs(limit: int = 200) -> List[Dict[str, Any]]:
    sb = get_supabase()

    try:
        res = (
            sb.table("usage_logs")
            .select("id, user_id, action, bytes_in, bytes_out, created_at")
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )

        raw = res.data if isinstance(res.data, list) else []
        return [row for row in raw if isinstance(row, dict)]

    except Exception as exc:
        st.error(f"Failed to fetch logs: {exc}")
        return []


# ---------------------------------------------------------
# MAIN ADMIN ANALYTICS PAGE
# ---------------------------------------------------------
def render() -> None:
    require_admin()

    st.title("Usage Analytics")

    # ---------------------------------------------------------
    # Filters
    # ---------------------------------------------------------
    st.subheader("Filters")

    limit = st.slider("Number of logs to load", 50, 500, 200, step=50)

    logs = _fetch_logs(limit)

    if not logs:
        st.info("No logs found.")
        return

    df = pd.DataFrame(logs)

    # ---------------------------------------------------------
    # Optional search
    # ---------------------------------------------------------
    search_term = st.text_input("Search logs (action, user_id, etc.)")

    if search_term:
        search_lower = search_term.lower()
        df = df[
            df.apply(
                lambda row: any(
                    search_lower in str(value).lower() for value in row.values
                ),
                axis=1,
            )
        ]

    # ---------------------------------------------------------
    # Logs Table
    # ---------------------------------------------------------
    st.subheader("Usage Logs")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # ---------------------------------------------------------
    # Inspect single log
    # ---------------------------------------------------------
    st.subheader("Inspect Log Entry")

    ids = df["id"].astype(str).tolist()
    selected_id = st.selectbox("Select Log ID", ids, key="analytics_log_select")

    selected = df[df["id"].astype(str) == selected_id]

    if not selected.empty:
        st.json(selected.iloc[0].to_dict())
