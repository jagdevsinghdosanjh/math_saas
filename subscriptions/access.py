import streamlit as st
from typing import Any, Dict

from subscriptions.core import get_active_subscription


def require_student_logged_in() -> Dict[str, Any]:
    student = st.session_state.get("student")
    if not student:
        st.error("Please login as student.")
        st.stop()
    return student


def require_active_subscription():
    student = require_student_logged_in()
    user_id = student["id"]

    sub = get_active_subscription(user_id)

    if not sub:
        st.warning("You need an active subscription to access this content.")
        st.info("Please go to the Subscription tab to upgrade.")
        st.stop()

    return sub