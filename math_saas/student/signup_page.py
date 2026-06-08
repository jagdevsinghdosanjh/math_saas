# math_saas/student/signup_page.py

import streamlit as st
from typing import Dict, Optional, Any #noqa

from math_saas.utils.db import get_supabase
from math_saas.subscriptions.core import create_subscription #noqa
from math_saas.auth import TEXT_MUTED #noqa


def render_signup_page() -> None:
    st.header("Create Student Account")

    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    grade = st.selectbox("Grade", ["9", "10"])
    board = st.selectbox("Board", ["CBSE", "ICSE", "STATE"])

    if st.button("Create Account"):
        sb = get_supabase()

        # ---------------------------------------------------------
        # STEP 1 — CREATE AUTH USER
        # ---------------------------------------------------------
        try:
            res = sb.auth.sign_up({"email": email, "password": password})
            user = res.user
        except Exception as exc:
            st.error(f"Signup failed: {exc}")
            return

        if not user:
            st.error("Signup failed.")
            return

        user_id = str(user.id)

        # ---------------------------------------------------------
        # STEP 2 — CHECK IF PROFILE ALREADY EXISTS
        # ---------------------------------------------------------
        try:
            existing = (
                sb.table("profiles")
                .select("id")
                .eq("id", user_id)
                .execute()
                .data
            )
        except Exception as exc:
            st.error(f"Error checking existing profile: {exc}")
            return

        # ---------------------------------------------------------
        # STEP 3 — CREATE PROFILE IF NOT EXISTS
        # ---------------------------------------------------------
        if not existing:
            try:
                sb.table("profiles").insert(
                    {
                        "id": user_id,
                        "email": email,
                        "full_name": full_name,
                        "grade": grade,
                        "board": board,
                        "is_admin": False,
                        "subscription_status": "free",
                        "role": "student",
                    }
                ).execute()
            except Exception as exc:
                st.error(f"Profile creation failed: {exc}")
                return

        # ---------------------------------------------------------
        # STEP 4 — CREATE FREE SUBSCRIPTION (ONLY IF NONE EXISTS)
        # ---------------------------------------------------------
        try:
            sb.table("subscriptions").insert(
                {
                    "user_id": user_id,
                    "plan_code": "FREE",
                    "status": "active",
                    "amount": 0,
                    "currency": "INR",
                }
            ).execute()
        except Exception:
            # Ignore duplicate subscription errors
            pass

        # ---------------------------------------------------------
        # SUCCESS
        # ---------------------------------------------------------
        st.success("Account created successfully! Please log in.")
        st.session_state["login_mode"] = "student"
        st.rerun()

# # math_saas/student/signup_page.py

# import streamlit as st
# from math_saas.utils.db import get_supabase
# from math_saas.subscriptions.core import create_subscription


# def render_signup_page():
#     st.header("Create Student Account")

#     full_name = st.text_input("Full Name")
#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")
#     grade = st.selectbox("Grade", ["9", "10"])
#     board = st.selectbox("Board", ["CBSE", "ICSE", "STATE"])

#     if st.button("Create Account"):
#         sb = get_supabase()

#         # Step 1 — Auth user
#         try:
#             res = sb.auth.sign_up({"email": email, "password": password})
#             user = res.user
#         except Exception as exc:
#             st.error(f"Signup failed: {exc}")
#             return

#         if not user:
#             st.error("Signup failed.")
#             return

#         # Step 2 — Profile
#         try:
#             sb.table("profiles").insert(
#                 {
#                     "id": user.id,
#                     "email": email,
#                     "full_name": full_name,
#                     "grade": grade,
#                     "board": board,
#                     "is_admin": False,
#                     "subscription_status": "free",
#                     "role": "student",
#                 }
#             ).execute()
#         except Exception as exc:
#             st.error(f"Profile creation failed: {exc}")
#             return

#         # Step 3 — Free subscription
#         create_subscription(
#             user_id=user.id,
#             plan_code="FREE",
#             status="active",
#             amount=0,
#             currency="INR",
#         )

#         st.success("Account created successfully! Please log in.")
#         st.session_state["login_mode"] = "student"
#         st.rerun()

# # import streamlit as st
# # from math_saas.utils.db import get_supabase
# # from math_saas.subscriptions.core import create_subscription


# # def render_signup_page():
# #     st.header("Create Student Account")

# #     full_name = st.text_input("Full Name")
# #     email = st.text_input("Email")
# #     password = st.text_input("Password", type="password")
# #     grade = st.selectbox("Grade", ["9", "10"])
# #     board = st.selectbox("Board", ["CBSE", "ICSE", "STATE"])

# #     if st.button("Create Account"):
# #         sb = get_supabase()

# #         # Step 1 — Create Auth User
# #         try:
# #             res = sb.auth.sign_up({"email": email, "password": password})
# #             user = res.user
# #         except Exception as exc:
# #             st.error(f"Signup failed: {exc}")
# #             return

# #         if not user:
# #             st.error("Signup failed.")
# #             return

# #         # Step 2 — Create Profile Row
# #         try:
# #             sb.table("profiles").insert({
# #                 "id": user.id,
# #                 "email": email,
# #                 "full_name": full_name,
# #                 "grade": grade,
# #                 "board": board,
# #                 "is_admin": False,
# #                 "subscription_status": "free"
# #             }).execute()
# #         except Exception as exc:
# #             st.error(f"Profile creation failed: {exc}")
# #             return

# #         # Step 3 — Create Free Subscription
# #         create_subscription(
# #             user_id=user.id,
# #             plan_code="FREE",
# #             status="active",
# #             amount=0,
# #             currency="INR"
# #         )

# #         st.success("Account created successfully! Please log in.")
# #         st.session_state["login_mode"] = "student"
# #         st.rerun()
