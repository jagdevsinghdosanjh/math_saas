import streamlit as st
from math_saas.auth import require_admin
from math_saas.utils.db import get_supabase
from math_saas.admin import users, subscriptions, chapters, analytics, settings

sb=get_supabase()

def run_admin():
    require_admin()  # ensures login first

    st.title("Math Hub Admin Panel")

    page = st.sidebar.radio(
        "Admin Menu",
        ["Users", "Subscriptions", "Chapters", "Analytics", "Settings"],
    )

    if page == "Users":
        users.render()
    elif page == "Subscriptions":
        subscriptions.render()
    elif page == "Chapters":
        chapters.render()
    elif page == "Analytics":
        analytics.render()
    elif page == "Settings":
        settings.render()

# import streamlit as st
# from math_saas.auth import require_admin
# from math_saas.admin import users, subscriptions, chapters, analytics, settings

# def run_admin():
#     st.title("Math Hub Admin Panel")
#     require_admin()

#     page = st.sidebar.radio(
#         "Admin Menu",
#         ["Users", "Subscriptions", "Chapters", "Analytics", "Settings"],
#     )

#     if page == "Users":
#         users.render()
#     elif page == "Subscriptions":
#         subscriptions.render()
#     elif page == "Chapters":
#         chapters.render()
#     elif page == "Analytics":
#         analytics.render()
#     elif page == "Settings":
#         settings.render()
