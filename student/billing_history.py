import streamlit as st
from typing import Any, Dict, List

from utils.db import get_supabase, require_user
from subscriptions.utils import format_inr, plan_name
from auth import TEXT_MUTED


# ---------------------------------------------------------
# FETCH USER SUBSCRIPTIONS (SCHEMA-SAFE)
# ---------------------------------------------------------
def _fetch_user_subscriptions(user_id: str) -> List[Dict[str, Any]]:
    sb = get_supabase()

    try:
        res = (
            sb.table("subscriptions")
            .select(
                "plan_code, status, amount, started_at, expires_at, razorpay_order_id"
            )
            .eq("user_id", user_id)
            .order("started_at", desc=True)
            .execute()
        )

        raw = res.data or []
        return [row for row in raw if isinstance(row, dict)]

    except Exception as exc:
        st.error(f"Error loading billing history: {exc}")
        return []


# ---------------------------------------------------------
# MAIN RENDER FUNCTION (UNIFIED AUTH + TYPE SAFE)
# ---------------------------------------------------------
def render_billing_history() -> None:
    st.header("Billing History")

    # Unified login model
    user_dict: Dict[str, Any] = require_user()

    user_id: str = str(user_dict.get("id", ""))
    if not user_id:
        st.error("Invalid student session.")
        return

    subs: List[Dict[str, Any]] = _fetch_user_subscriptions(user_id)

    if not subs:
        st.info("No billing history yet.")
        return

    # Render each subscription as a neon card
    for s in subs:
        plan = plan_name(str(s.get("plan_code", "")))
        status = str(s.get("status", ""))
        amount = format_inr(s.get("amount", 0))
        started = str(s.get("started_at", ""))
        expires = str(s.get("expires_at", ""))
        order_id = str(s.get("razorpay_order_id", ""))

        st.markdown(
            f"""
            <div class="neon-card" style="margin-bottom:16px;">
                <h4>{plan}</h4>
                <p style="color:{TEXT_MUTED}; margin-bottom:6px;">
                    Status: {status}<br>
                    Amount: {amount}<br>
                    Started: {started}<br>
                    Expires: {expires}<br>
                    Order ID: {order_id}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# import streamlit as st
# from typing import Any, Dict, List

# from utils.db import get_supabase
# from subscriptions.utils import format_inr, plan_name
# from auth import TEXT_MUTED


# # ---------------------------------------------------------
# # FETCH USER SUBSCRIPTIONS (SCHEMA-SAFE)
# # ---------------------------------------------------------
# def _fetch_user_subscriptions(user_id: str) -> List[Dict[str, Any]]:
#     sb = get_supabase()

#     try:
#         # Only select columns that ACTUALLY exist in your Supabase table
#         res = (
#             sb.table("subscriptions")
#             .select(
#                 "plan_code, status, amount, started_at, expires_at, razorpay_order_id"
#             )
#             .eq("user_id", user_id)
#             .order("started_at", desc=True)
#             .execute()
#         )

#         raw = res.data or []
#         return [row for row in raw if isinstance(row, dict)]

#     except Exception as exc:
#         st.error(f"Error loading billing history: {exc}")
#         return []


# # ---------------------------------------------------------
# # MAIN RENDER FUNCTION
# # ---------------------------------------------------------
# def render_billing_history() -> None:
#     st.header("Billing History")

#     student = st.session_state.get("student")
#     if not isinstance(student, dict):
#         st.error("Please login as student.")
#         return

#     user_id = str(student.get("id") or "")
#     if not user_id:
#         st.error("Invalid student session.")
#         return

#     subs = _fetch_user_subscriptions(user_id)

#     if not subs:
#         st.info("No billing history yet.")
#         return

#     # Render each subscription as a neon card
#     for s in subs:
#         plan = plan_name(str(s.get("plan_code", "")))
#         status = str(s.get("status", ""))
#         amount = format_inr(s.get("amount", 0))
#         started = str(s.get("started_at", ""))
#         expires = str(s.get("expires_at", ""))
#         order_id = str(s.get("razorpay_order_id", ""))

#         st.markdown(
#             f"""
#             <div class="neon-card" style="margin-bottom:16px;">
#                 <h4>{plan}</h4>
#                 <p style="color:{TEXT_MUTED}; margin-bottom:6px;">
#                     Status: {status}<br>
#                     Amount: {amount}<br>
#                     Started: {started}<br>
#                     Expires: {expires}<br>
#                     Order ID: {order_id}
#                 </p>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )
