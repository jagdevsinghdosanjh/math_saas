﻿import streamlit as st

from auth import require_admin

# Admin modules
from admin.subscriptions_admin import render as render_subscriptions
from admin.analytics import render as render_analytics
from admin.billing import render as render_billing
from admin.chapters import render as render_chapters
from admin.users import render as render_users
from admin.pdf_notes import render as render_pdf_notes
from admin.videos import render as render_videos
from admin.settings import render as render_settings


# -----------------------------
# Admin App Router
# -----------------------------
def run_admin():
    require_admin()

    st.title("Admin Dashboard")

    menu = st.sidebar.radio(
        "Navigation",
        [
            "Analytics",
            "Subscriptions",
            "Billing",
            "Chapters",
            "Users",
            "PDF Notes",
            "Videos",
            "Settings",
        ]
    )

    if menu == "Analytics":
        render_analytics()

    elif menu == "Subscriptions":
        render_subscriptions()

    elif menu == "Billing":
        render_billing()

    elif menu == "Chapters":
        render_chapters()

    elif menu == "Users":
        render_users()

    elif menu == "PDF Notes":
        render_pdf_notes()

    elif menu == "Videos":
        render_videos()

    elif menu == "Settings":
        render_settings()

# import streamlit as st
# from typing import Any, Dict, List

# from math_saas.utils.db import get_supabase
# from math_saas.subscriptions.plans import PLANS #noqa


# # -----------------------------
# # Fetch all subscriptions
# # -----------------------------
# def _fetch_all() -> List[Dict[str, Any]]:
#     sb = get_supabase()
#     res = sb.table("subscriptions").select("*").execute()
#     raw = res.data or []
#     return [item for item in raw if isinstance(item, dict)]


# # -----------------------------
# # Compute MRR (Monthly Recurring Revenue)
# # -----------------------------
# def compute_mrr(subs: List[Dict[str, Any]]) -> int:
#     monthly = [
#         s for s in subs
#         if s.get("plan_code") == "MONTHLY" and s.get("status") == "active"
#     ]
#     return sum(s.get("amount", 0) for s in monthly)


# # -----------------------------
# # Compute ARR (Annual Recurring Revenue)
# # -----------------------------
# def compute_arr(subs: List[Dict[str, Any]]) -> int:
#     annual = [
#         s for s in subs
#         if s.get("plan_code") == "ANNUAL" and s.get("status") == "active"
#     ]
#     return sum(s.get("amount", 0) for s in annual)


# # -----------------------------
# # Count active subscribers
# # -----------------------------
# def count_active(subs: List[Dict[str, Any]]) -> int:
#     return sum(1 for s in subs if s.get("status") == "active")


# # -----------------------------
# # Count expired subscribers
# # -----------------------------
# def count_expired(subs: List[Dict[str, Any]]) -> int:
#     return sum(1 for s in subs if s.get("status") == "expired")


# # -----------------------------
# # Plan distribution
# # -----------------------------
# def plan_distribution(subs: List[Dict[str, Any]]) -> Dict[str, int]:
#     dist = {"FREE": 0, "MONTHLY": 0, "ANNUAL": 0}
#     for s in subs:
#         code = s.get("plan_code")
#         if code in dist:
#             dist[code] += 1
#     return dist


# # -----------------------------
# # Render Analytics Dashboard
# # -----------------------------
# def render():
#     st.title("Subscription Analytics")

#     subs = _fetch_all()

#     if not subs:
#         st.info("No subscription data available.")
#         return

#     st.subheader("Key Metrics")

#     mrr = compute_mrr(subs)
#     arr = compute_arr(subs)
#     active = count_active(subs)
#     expired = count_expired(subs)
#     dist = plan_distribution(subs)

#     st.metric("Active Subscribers", active)
#     st.metric("Expired Subscribers", expired)
#     st.metric("MRR (₹)", mrr / 100)
#     st.metric("ARR (₹)", arr / 100)

#     st.subheader("Plan Distribution")
#     st.json(dist)

#     st.subheader("Raw Subscription Data")
#     st.dataframe(subs, use_container_width=True, hide_index=True)

# # import streamlit as st
# # from math_saas.auth import require_admin
# # from math_saas.utils.db import get_supabase
# # from math_saas.admin import users, subscriptions, chapters, analytics, settings

# # sb=get_supabase()

# # def run_admin():
# #     require_admin()  # ensures login first

# #     st.title("Math Hub Admin Panel")

# #     page = st.sidebar.radio(
# #         "Admin Menu",
# #         ["Users", "Subscriptions", "Chapters", "Analytics", "Settings"],
# #     )

# #     if page == "Users":
# #         users.render()
# #     elif page == "Subscriptions":
# #         subscriptions.render()
# #     elif page == "Chapters":
# #         chapters.render()
# #     elif page == "Analytics":
# #         analytics.render()
# #     elif page == "Settings":
# #         settings.render()

# # # import streamlit as st
# # # from math_saas.auth import require_admin
# # # from math_saas.admin import users, subscriptions, chapters, analytics, settings

# # # def run_admin():
# # #     st.title("Math Hub Admin Panel")
# # #     require_admin()

# # #     page = st.sidebar.radio(
# # #         "Admin Menu",
# # #         ["Users", "Subscriptions", "Chapters", "Analytics", "Settings"],
# # #     )

# # #     if page == "Users":
# # #         users.render()
# # #     elif page == "Subscriptions":
# # #         subscriptions.render()
# # #     elif page == "Chapters":
# # #         chapters.render()
# # #     elif page == "Analytics":
# # #         analytics.render()
# # #     elif page == "Settings":
# # #         settings.render()
