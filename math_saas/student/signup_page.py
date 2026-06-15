# math_saas/student/signup_page.py

import streamlit as st
from math_saas.utils.db import get_supabase


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
        # STEP 0 — CHECK IF EMAIL ALREADY EXISTS
        # ---------------------------------------------------------
        try:
            res = sb.auth.admin.list_users()
            users = getattr(res, "users", [])

            for u in users:
                if isinstance(u, dict) and u.get("email") == email:
                    st.error("Email already registered. Please log in instead.")
                    return
        except Exception:
            pass  # admin API may be restricted

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
            existing_profile = (
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
        if not existing_profile:
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
        # STEP 4 — CREATE FREE SUBSCRIPTION (DIRECT DB INSERT)
        # ---------------------------------------------------------
        try:
            existing_sub = (
                sb.table("subscriptions")
                .select("id")
                .eq("user_id", user_id)
                .eq("plan_code", "FREE")
                .execute()
                .data
            )
        except Exception:
            existing_sub = []

        if not existing_sub:
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
                pass  # ignore duplicate subscription errors

        # ---------------------------------------------------------
        # SUCCESS
        # ---------------------------------------------------------
        st.success("Account created successfully! Please log in.")
        st.session_state["login_mode"] = "student"
        st.rerun()
