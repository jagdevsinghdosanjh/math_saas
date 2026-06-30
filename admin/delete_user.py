import streamlit as st
from utils.db import get_supabase, get_supabase_admin

def delete_user(user_id: str):
    sb = get_supabase()
    admin = get_supabase_admin()

    # 1. Delete from Supabase Auth
    try:
        admin.auth.admin.delete_user(user_id)
    except Exception as exc:
        st.error(f"Failed to delete auth user: {exc}")
        return False

    # 2. Delete from profiles table (subscriptions auto-delete via CASCADE)
    try:
        sb.table("profiles").delete().eq("id", user_id).execute()
    except Exception as exc:
        st.error(f"Failed to delete profile: {exc}")
        return False

    st.success("User deleted successfully.")
    return True
