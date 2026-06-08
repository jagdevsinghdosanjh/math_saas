import streamlit as st
from math_saas.utils.db import get_supabase


def render_subscription_page():
    """Student subscription page with Free Plan + Upgrade options."""
    sb = get_supabase()

    student = st.session_state.get("student")
    if not student:
        st.error("You must be logged in as a student.")
        return

    student_id = student["id"]

    # Fetch subscription
    try:
        res = (
            sb.table("subscriptions")
            .select("*")
            .eq("user_id", student_id)
            .single()
            .execute()
        )
        sub = res.data
    except Exception:
        sub = None

    st.markdown("<h2>Your Subscription</h2>", unsafe_allow_html=True)

    # -----------------------------
    # CASE 1: No subscription → assign FREE PLAN
    # -----------------------------
    if not sub:
        st.info("You are currently on the Free Plan.")

        if st.button("Activate Free Plan"):
            try:
                sb.table("subscriptions").insert(
                    {
                        "user_id": student_id,
                        "plan_name": "free",
                        "is_active": True,
                        "payment_id": None,
                    }
                ).execute()
                st.success("Free Plan activated.")
                st.rerun()
            except Exception as exc:
                st.error(f"Failed to activate free plan: {exc}")
        return

    # -----------------------------
    # CASE 2: Already subscribed
    # -----------------------------
    st.success(f"Current Plan: {sub['plan_name'].upper()}")

    if sub["plan_name"] == "free":
        st.warning("You are on the Free Plan. Upgrade to unlock premium content.")

        if st.button("Upgrade to Premium"):
            st.session_state["upgrade_mode"] = True
            st.rerun()

    else:
        st.info("You already have a premium subscription.")

    # -----------------------------
    # Razorpay Upgrade Flow
    # -----------------------------
    if st.session_state.get("upgrade_mode"):
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h3>Upgrade to Premium</h3>", unsafe_allow_html=True)

        st.write("Choose a plan:")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("₹199 / Month"):
                st.session_state["selected_plan"] = "monthly"
                st.rerun()

        with col2:
            if st.button("₹999 / Year"):
                st.session_state["selected_plan"] = "yearly"
                st.rerun()

        plan = st.session_state.get("selected_plan")
        if plan:
            st.info(f"You selected: {plan.upper()} plan")

            if st.button("Proceed to Payment"):
                st.write("Redirecting to Razorpay checkout...")
                # Razorpay integration will go here
