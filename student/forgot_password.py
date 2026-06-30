import streamlit as st
from utils.db import get_supabase

def render_forgot_password_page():
    st.markdown("### Recover Account")

    st.info("Enter your registered email to reset your password.")

    email = st.text_input("Registered Email")

    if st.button("Send Password Reset Link"):
        if not email:
            st.error("Please enter your email.")
            return

        sb = get_supabase()

        try:
            sb.auth.reset_password_email(email)
            st.success(
                "A password reset link has been sent to your email. "
                "Please check your inbox."
            )
        except Exception as exc:
            st.error(f"Failed to send reset link. {exc}")

    st.markdown("---")
    st.markdown("### Recover User ID")

    if st.button("Show My User ID"):
        if not email:
            st.error("Enter your email first.")
            return

        sb = get_supabase()

        res = (
            sb.table("profiles")
            .select("id")
            .eq("email", email)
            .maybe_single()
            .execute()
        )

        data = res.data if res else None

        if not data:
            st.error("No user found with this email.")
            return

        st.success(f"Your User ID is: **{data.get('id')}**")
