import streamlit as st
from typing import Any, Dict, List

from math_saas.auth import require_admin
from math_saas.utils.db import get_supabase


# ---------------------------------------------------------
# FETCH SETTINGS (TYPE-SAFE)
# ---------------------------------------------------------
def _fetch_settings() -> List[Dict[str, Any]]:
    sb = get_supabase()

    try:
        res = (
            sb.table("settings")
            .select("id, key, value, updated_at, created_at")
            .order("key", desc=False)
            .execute()
        )
        raw = res.data or []
        return [row for row in raw if isinstance(row, dict)]

    except Exception as exc:
        st.error(f"Failed to fetch settings: {exc}")
        return []


# ---------------------------------------------------------
# MAIN ADMIN SETTINGS PAGE
# ---------------------------------------------------------
def render():
    require_admin()

    st.title("System Settings")

    # -----------------------------
    # DISPLAY EXISTING SETTINGS
    # -----------------------------
    settings = _fetch_settings()

    st.subheader("All Settings")

    if not settings:
        st.info("No settings found.")
    else:
        st.dataframe(settings, width="stretch", hide_index=True)

    # -----------------------------
    # UPDATE / ADD SETTING
    # -----------------------------
    st.subheader("Add or Update Setting")

    with st.form("update_setting_form"):
        key = st.text_input("Key (unique identifier)")
        value = st.text_input("Value")

        submit = st.form_submit_button("Save Setting")

        if submit:
            key_clean = (key or "").strip()
            value_clean = (value or "").strip()

            if not key_clean:
                st.error("Key cannot be empty.")
                return

            if not value_clean:
                st.error("Value cannot be empty.")
                return

            sb = get_supabase()

            try:
                sb.table("settings").upsert(
                    {
                        "key": key_clean,
                        "value": value_clean,
                    }
                ).execute()

                st.success("Setting saved successfully.")
                st.rerun()

            except Exception as exc:
                st.error(f"Failed to save setting: {exc}")
