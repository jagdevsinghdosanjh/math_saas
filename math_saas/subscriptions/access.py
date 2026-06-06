import streamlit as st
from typing import Any, Dict

from math_saas.subscriptions.core import get_active_subscription


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

# import datetime as dt
# import streamlit as st
# from typing import Any, Dict, List, Optional

# from math_saas.utils.db import get_supabase


# # -----------------------------
# # Fetch active subscription
# # -----------------------------
# def get_active_subscription(user_id: str) -> Optional[Dict[str, Any]]:
#     sb = get_supabase()

#     now_iso = dt.datetime.utcnow().isoformat()

#     res = (
#         sb.table("subscriptions")
#         .select("*")
#         .eq("user_id", user_id)
#         .eq("status", "active")
#         .gte("expires_at", now_iso)
#         .order("expires_at", desc=True)
#         .limit(1)
#         .execute()
#     )

#     raw = res.data or []

#     # Pylance-safe filtering
#     data: List[Dict[str, Any]] = [
#         item for item in raw if isinstance(item, dict)
#     ]

#     return data[0] if data else None


# # -----------------------------
# # Require student login
# # -----------------------------
# def require_student_logged_in() -> Dict[str, Any]:
#     student = st.session_state.get("student")

#     if not student:
#         st.error("Please login as student.")
#         st.stop()

#     return student


# # -----------------------------
# # Require active subscription
# # -----------------------------
# def require_active_subscription():
#     student = require_student_logged_in()
#     user_id = student["id"]

#     sub = get_active_subscription(user_id)

#     if not sub:
#         st.warning("You need an active subscription to access this content.")
#         st.info("Please go to the Subscription tab to upgrade.")
#         st.stop()

#     return sub

# # import datetime as dt
# # import streamlit as st
# # from math_saas.utils.db import get_supabase

# # def get_active_subscription(user_id: str):
# #     sb = get_supabase()
# #     today = dt.datetime.utcnow().isoformat()
# #     res = (
# #         sb.table("subscriptions")
# #         .select("*")
# #         .eq("user_id", user_id)
# #         .eq("status", "active")
# #         .gte("expires_at", today)
# #         .order("expires_at", desc=True)
# #         .limit(1)
# #         .execute()
# #     )
# #     data = res.data or []
# #     return data[0] if data else None


# # def require_active_subscription():
# #     user = st.session_state.get("student")
# #     if not user:
# #         st.error("Please login as student first.")
# #         st.stop()

# #     sub = get_active_subscription(user["id"])
# #     if not sub:
# #         st.warning("You don't have an active subscription. Please subscribe to continue.")
# #         st.stop()
