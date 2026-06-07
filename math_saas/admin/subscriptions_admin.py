import streamlit as st
from typing import Any, Dict, List

from math_saas.auth import require_admin
from math_saas.utils.db import get_supabase
from math_saas.subscriptions.core import (
    get_latest_subscription,#noqa
    get_active_subscription,#noqa
)


def _fetch_subscriptions(status_filter: str) -> List[Dict[str, Any]]:
    sb = get_supabase()

    query = (
        sb.table("subscriptions")
        .select("*")
        .order("started_at", desc=True)
    )

    if status_filter != "all":
        query = query.eq("status", status_filter)

    res = query.execute()
    raw = res.data or []

    return [item for item in raw if isinstance(item, dict)]


def render():
    require_admin()

    st.title("Subscription Management")

    status_filter = st.selectbox(
        "Status",
        ["all", "active", "pending", "expired", "failed"],
        index=0,
    )

    subs = _fetch_subscriptions(status_filter)

    if not subs:
        st.info("No subscriptions found.")
        return

    st.dataframe(subs, width="stretch", hide_index=True)

    st.subheader("Inspect Subscription")

    ids = [str(s["id"]) for s in subs]
    selected_id = st.selectbox("Select Subscription ID", ids)

    selected = next((s for s in subs if str(s["id"]) == selected_id), None)

    if selected:
        st.json(selected)

# import streamlit as st
# from typing import Any, Dict, List

# from math_saas.auth import require_admin
# from math_saas.utils.db import get_supabase


# # -----------------------------
# # Fetch all subscriptions
# # -----------------------------
# def _fetch_subscriptions(status_filter: str) -> List[Dict[str, Any]]:
#     sb = get_supabase()

#     query = (
#         sb.table("subscriptions")
#         .select(
#             "id, user_id, plan_code, status, amount, currency, "
#             "started_at, expires_at, razorpay_order_id, razorpay_payment_id"
#         )
#         .order("started_at", desc=True)
#     )

#     if status_filter != "all":
#         query = query.eq("status", status_filter)

#     res = query.execute()

#     raw = res.data or []

#     # Pylance-safe filtering
#     data: List[Dict[str, Any]] = [
#         item for item in raw if isinstance(item, dict)
#     ]

#     return data


# # -----------------------------
# # Admin Subscription Dashboard
# # -----------------------------
# def render():
#     require_admin()

#     st.title("Subscription Management")

#     st.subheader("Filter Subscriptions")

#     status_filter = st.selectbox(
#         "Status",
#         ["all", "active", "pending", "expired", "failed"],
#         index=0,
#     )

#     subs = _fetch_subscriptions(status_filter)

#     if not subs:
#         st.info("No subscriptions found for this filter.")
#         return

#     st.subheader("Subscriptions")

#     st.dataframe(
#         subs,
#         width="stretch",
#         hide_index=True,
#     )

#     # Optional: Show details of a selected subscription
#     st.subheader("Inspect Subscription")

#     ids = [str(s["id"]) for s in subs]
#     selected_id = st.selectbox("Select Subscription ID", ids)

#     selected = next((s for s in subs if str(s["id"]) == selected_id), None)

#     if selected:
#         st.json(selected)
