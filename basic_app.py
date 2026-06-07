﻿﻿﻿﻿﻿﻿﻿import streamlit as st

from math_saas.auth import logout, app_container_style
from math_saas.admin.admin_app import run_admin
from math_saas.student.student_app import run_student
from math_saas.utils.db import get_supabase


# -----------------------------
# SAFE QUERY PARAM ACCESS
# -----------------------------
def get_param(params, key):
    return params[key] if key in params else None


# -----------------------------
# ADMIN LOGIN FORM
# -----------------------------
def admin_login_form():
    st.markdown("<h3>Admin Login</h3>", unsafe_allow_html=True)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login as Admin"):
        sb = get_supabase()

        try:
            res = sb.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
        except Exception:
            st.error("Invalid login credentials")
            return

        user = res.user
        if not user:
            st.error("Invalid login credentials")
            return

        profile = (
            sb.table("profiles")
            .select("*")
            .eq("id", user.id)
            .single()
            .execute()
            .data
        )

        if not profile or not profile.get("is_admin"):
            st.error("You are not an admin.")
            return

        st.session_state["admin"] = profile
        st.success("Admin login successful.")
        st.rerun()


# -----------------------------
# STUDENT LOGIN FORM
# -----------------------------
def student_login_form():
    st.markdown("<h3>Student Login</h3>", unsafe_allow_html=True)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login as Student"):
        sb = get_supabase()

        try:
            res = sb.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
        except Exception:
            st.error("Invalid login credentials")
            return

        user = res.user
        if not user:
            st.error("Invalid login credentials")
            return

        profile = (
            sb.table("profiles")
            .select("*")
            .eq("id", user.id)
            .single()
            .execute()
            .data
        )

        if not profile or profile.get("is_admin"):
            st.error("Students must login from Student Login.")
            return

        st.session_state["student"] = profile
        st.success("Student login successful.")
        st.rerun()


# -----------------------------
# MAIN APP ROUTER
# -----------------------------
def main():
    app_container_style()

    params = st.query_params

    # SAFE ACCESS (no .get())
    admin_logout_flag = get_param(params, "admin_logout")
    student_logout_flag = get_param(params, "student_logout")

    if admin_logout_flag == "true":
        logout()
    if student_logout_flag == "true":
        logout()

    # If admin logged in → go to admin panel
    if isinstance(st.session_state.get("admin"), dict):
        run_admin()
        return

    # If student logged in → go to student panel
    if isinstance(st.session_state.get("student"), dict):
        run_student()
        return

    # Otherwise show login gateway
    st.markdown(
        """
        <h2 style="margin-top:0;">Welcome to Math Hub</h2>
        <p style="color:#9ca3af;">Choose your login type to continue.</p>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Admin Login"):
            st.session_state["login_mode"] = "admin"
            st.rerun()

    with col2:
        if st.button("Student Login"):
            st.session_state["login_mode"] = "student"
            st.rerun()

    mode = st.session_state.get("login_mode")

    if mode == "admin":
        admin_login_form()
    elif mode == "student":
        student_login_form()


if __name__ == "__main__":
    main()

# import streamlit as st

# from math_saas.auth import logout, app_container_style
# from math_saas.admin.admin_app import run_admin
# from math_saas.student.student_app import run_student
# from math_saas.utils.db import get_supabase


# # -----------------------------
# # ADMIN LOGIN FORM
# # -----------------------------
# def admin_login_form():
#     st.markdown("<h3>Admin Login</h3>", unsafe_allow_html=True)

#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")

#     if st.button("Login as Admin"):
#         sb = get_supabase()

#         try:
#             res = sb.auth.sign_in_with_password(
#                 {"email": email, "password": password}
#             )
#         except Exception:
#             st.error("Invalid login credentials")
#             return

#         user = res.user
#         if not user:
#             st.error("Invalid login credentials")
#             return

#         profile = (
#             sb.table("profiles")
#             .select("*")
#             .eq("id", user.id)
#             .single()
#             .execute()
#             .data
#         )

#         if not profile or not profile.get("is_admin"):
#             st.error("You are not an admin.")
#             return

#         st.session_state["admin"] = profile
#         st.success("Admin login successful.")
#         st.rerun()


# # -----------------------------
# # STUDENT LOGIN FORM
# # -----------------------------
# def student_login_form():
#     st.markdown("<h3>Student Login</h3>", unsafe_allow_html=True)

#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")

#     if st.button("Login as Student"):
#         sb = get_supabase()

#         try:
#             res = sb.auth.sign_in_with_password(
#                 {"email": email, "password": password}
#             )
#         except Exception:
#             st.error("Invalid login credentials")
#             return

#         user = res.user
#         if not user:
#             st.error("Invalid login credentials")
#             return

#         profile = (
#             sb.table("profiles")
#             .select("*")
#             .eq("id", user.id)
#             .single()
#             .execute()
#             .data
#         )

#         if not profile or profile.get("is_admin"):
#             st.error("Students must login from Student Login.")
#             return

#         st.session_state["student"] = profile
#         st.success("Student login successful.")
#         st.rerun()


# # -----------------------------
# # MAIN APP ROUTER
# # -----------------------------
# def main():
#     app_container_style()

#     params = st.query_params

#     # Safe access for logout flags
#     admin_logout_flag = params.get("admin_logout", None)
#     student_logout_flag = params.get("student_logout", None)

#     if admin_logout_flag == "true":
#         logout()
#     if student_logout_flag == "true":
#         logout()

#     # If admin logged in → go to admin panel
#     if isinstance(st.session_state.get("admin"), dict):
#         run_admin()
#         return

#     # If student logged in → go to student panel
#     if isinstance(st.session_state.get("student"), dict):
#         run_student()
#         return

#     # Otherwise show login gateway
#     st.markdown(
#         """
#         <h2 style="margin-top:0;">Welcome to Math Hub</h2>
#         <p style="color:#9ca3af;">Choose your login type to continue.</p>
#         """,
#         unsafe_allow_html=True,
#     )

#     col1, col2 = st.columns(2)

#     with col1:
#         if st.button("Admin Login"):
#             st.session_state["login_mode"] = "admin"
#             st.rerun()

#     with col2:
#         if st.button("Student Login"):
#             st.session_state["login_mode"] = "student"
#             st.rerun()

#     mode = st.session_state.get("login_mode")

#     if mode == "admin":
#         admin_login_form()
#     elif mode == "student":
#         student_login_form()


# if __name__ == "__main__":
#     main()


# # import streamlit as st

# # from math_saas.auth import logout, app_container_style
# # from math_saas.auth import require_admin, require_student

# # from math_saas.admin.admin_app import run_admin
# # from math_saas.student.student_app import run_student

# # from math_saas.auth import TEXT_MUTED, TEXT_MAIN, ACCENT
# # from math_saas.utils.db import get_supabase


# # # -----------------------------
# # # ADMIN LOGIN FORM
# # # -----------------------------
# # def admin_login_form():
# #     st.markdown("<h3>Admin Login</h3>", unsafe_allow_html=True)

# #     email = st.text_input("Email")
# #     password = st.text_input("Password", type="password")

# #     if st.button("Login as Admin"):
# #         sb = get_supabase()

# #         try:
# #             res = sb.auth.sign_in_with_password(
# #                 {"email": email, "password": password}
# #             )
# #         except Exception:
# #             st.error("Invalid login credentials")
# #             return

# #         user = res.user
# #         if not user:
# #             st.error("Invalid login credentials")
# #             return

# #         # Fetch profile
# #         profile = (
# #             sb.table("profiles")
# #             .select("*")
# #             .eq("id", user.id)
# #             .single()
# #             .execute()
# #             .data
# #         )

# #         if not profile or not profile.get("is_admin"):
# #             st.error("You are not an admin.")
# #             return

# #         st.session_state["admin"] = profile
# #         st.success("Admin login successful.")
# #         st.rerun()


# # # -----------------------------
# # # STUDENT LOGIN FORM
# # # -----------------------------
# # def student_login_form():
# #     st.markdown("<h3>Student Login</h3>", unsafe_allow_html=True)

# #     email = st.text_input("Email")
# #     password = st.text_input("Password", type="password")

# #     if st.button("Login as Student"):
# #         sb = get_supabase()

# #         try:
# #             res = sb.auth.sign_in_with_password(
# #                 {"email": email, "password": password}
# #             )
# #         except Exception:
# #             st.error("Invalid login credentials")
# #             return

# #         user = res.user
# #         if not user:
# #             st.error("Invalid login credentials")
# #             return

# #         # Fetch profile
# #         profile = (
# #             sb.table("profiles")
# #             .select("*")
# #             .eq("id", user.id)
# #             .single()
# #             .execute()
# #             .data
# #         )

# #         if not profile or profile.get("is_admin"):
# #             st.error("Students must login from Student Login.")
# #             return

# #         st.session_state["student"] = profile
# #         st.success("Student login successful.")
# #         st.rerun()


# # # -----------------------------
# # # MAIN APP ROUTER
# # # -----------------------------
# # def main():
# #     app_container_style()

# #     # Handle logout
# #     if st.query_params.get("admin_logout") == "true":
# #         logout()
# #     if st.query_params.get("student_logout") == "true":
# #         logout()

# #     # If admin logged in → go to admin panel
# #     if st.session_state.get("admin"):
# #         run_admin()
# #         return

# #     # If student logged in → go to student panel
# #     if st.session_state.get("student"):
# #         run_student()
# #         return

# #     # Otherwise show login gateway
# #     st.markdown(
# #         """
# #         <h2 style="margin-top:0;">Welcome to Math Hub</h2>
# #         <p style="color:#9ca3af;">Choose your login type to continue.</p>
# #         """,
# #         unsafe_allow_html=True,
# #     )

# #     col1, col2 = st.columns(2)

# #     with col1:
# #         st.markdown(
# #             f"""
# #             <div class="neon-card">
# #                 <h4>Admin Login</h4>
# #                 <p style="color:{TEXT_MUTED};">Access admin dashboard, analytics, billing, and content management.</p>
# #             </div>
# #             """,
# #             unsafe_allow_html=True,
# #         )
# #         if st.button("Proceed as Admin"):
# #             st.session_state["login_mode"] = "admin"
# #             st.rerun()

# #     with col2:
# #         st.markdown(
# #             f"""
# #             <div class="neon-card">
# #                 <h4>Student Login</h4>
# #                 <p style="color:{TEXT_MUTED};">Access chapters, notes, subscription, and billing.</p>
# #             </div>
# #             """,
# #             unsafe_allow_html=True,
# #         )
# #         if st.button("Proceed as Student"):
# #             st.session_state["login_mode"] = "student"
# #             st.rerun()

# #     # Show login form based on selection
# #     mode = st.session_state.get("login_mode")
# #     if mode == "admin":
# #         admin_login_form()
# #     elif mode == "student":
# #         student_login_form()


# # if __name__ == "__main__":
# #     main()

# # # import streamlit as st
# # # from math_saas.admin.admin_app import run_admin
# # # from math_saas.student.student_app import run_student

# # # st.set_page_config(page_title="math-saas", layout="wide")

# # # run_admin()
