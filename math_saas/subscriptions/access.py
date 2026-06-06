import datetime as dt
import streamlit as st
from math_saas.utils.db import get_supabase

def get_active_subscription(user_id: str):
    sb = get_supabase()
    today = dt.datetime.utcnow().isoformat()
    res = (
        sb.table("subscriptions")
        .select("*")
        .eq("user_id", user_id)
        .eq("status", "active")
        .gte("expires_at", today)
        .order("expires_at", desc=True)
        .limit(1)
        .execute()
    )
    data = res.data or []
    return data[0] if data else None


def require_active_subscription():
    user = st.session_state.get("student")
    if not user:
        st.error("Please login as student first.")
        st.stop()

    sub = get_active_subscription(user["id"])
    if not sub:
        st.warning("You don't have an active subscription. Please subscribe to continue.")
        st.stop()
