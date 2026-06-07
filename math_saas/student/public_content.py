import streamlit as st
from math_saas.utils.db import get_supabase
from math_saas.utils.formatter import fix_math_rendering

def render_public_content():
    """Render public content with math auto‑formatting and safe type handling."""
    sb = get_supabase()

    try:
        res = sb.table("public_content").select("*").order("created_at", desc=True).execute()
        items_raw = res.data or []
    except Exception as e:
        st.error(f"Error fetching content: {e}")
        return

    items = [i for i in items_raw if isinstance(i, dict)]

    if not items:
        st.info("No public content available.")
        return

    for item in items:
        title = str(item.get("title", "Untitled"))
        body = str(item.get("body", ""))
        is_premium = bool(item.get("is_premium", False))

        # ✅ Auto‑fix math rendering and preserve LaTeX syntax
        body = fix_math_rendering(body).replace("\\\\", "\\")

        st.markdown(
            f"""
            <div class="neon-card" style="margin-bottom:16px;">
                <h4>{title}</h4>
                <p style="color:#a0a6b1; white-space:pre-wrap;">{body}</p>
                <p><strong>Premium:</strong> {is_premium}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ✅ Trigger MathJax rendering after content load
    st.markdown(
        """
        <script>
        const renderMath = () => {
          if (window.MathJax) MathJax.typesetPromise();
        };
        const observer = new MutationObserver(renderMath);
        observer.observe(document.body, { childList: true, subtree: true });
        renderMath();
        </script>
        """,
        unsafe_allow_html=True,
    )

# import streamlit as st
# from math_saas.utils.db import get_supabase
# from math_saas.utils.formatter import fix_math_rendering  # ✅ single import

# def render_public_content():
#     """Render public content with math auto‑formatting and safe type handling."""
#     sb = get_supabase()

#     try:
#         res = sb.table("public_content").select("*").order("created_at", desc=True).execute()
#         items_raw = res.data or []
#         st.write("Supabase client:", sb)
#         st.write("Query result:", res)

#     except Exception as e:
#         st.error(f"Error fetching content: {e}")
#         return

#     # ✅ Ensure items are dictionaries only
#     items = [i for i in items_raw if isinstance(i, dict)]

#     if not items:
#         st.info("No public content available.")
#         return

#     for item in items:
#         # ✅ Safe access using dict.get()
#         title = str(item.get("title", "Untitled"))
#         body = str(item.get("body", ""))
#         is_premium = bool(item.get("is_premium", False))

#         # ✅ Auto‑fix math rendering before display
#         body = fix_math_rendering(body)

#         st.markdown(
#             f"""
#             <div class="neon-card" style="margin-bottom:16px;">
#                 <h4>{title}</h4>
#                 <p style="color:#a0a6b1; white-space:pre-wrap;">{body}</p>
#                 <p><strong>Premium:</strong> {is_premium}</p>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )

# # import streamlit as st
# # from math_saas.utils.db import get_supabase
# # from math_saas.utils.formatter import fix_math_rendering  # ✅ new import
# # from math_saas.utils.formatter import fix_math_rendering

# # def render_public_content():
# #     # When displaying AI‑generated posts
# #     body = fix_math_rendering(body)
# #     st.markdown(body, unsafe_allow_html=True)


# #     """Render public content with math auto‑formatting and safe type handling."""
# #     sb = get_supabase()

# #     try:
# #         res = sb.table("public_content").select("*").order("created_at", desc=True).execute()
# #         items_raw = res.data or []
# #     except Exception as e:
# #         st.error(f"Error fetching content: {e}")
# #         return

# #     # ✅ Ensure items are dictionaries only
# #     items = [i for i in items_raw if isinstance(i, dict)]

# #     if not items:
# #         st.info("No public content available.")
# #         return

# #     for item in items:
# #         # ✅ Safe access using dict.get()
# #         title = str(item.get("title", "Untitled"))
# #         body = str(item.get("body", ""))
# #         is_premium = bool(item.get("is_premium", False))

# #         # ✅ Auto‑fix math rendering before display
# #         body = fix_math_rendering(body)

# #         st.markdown(
# #             f"""
# #             <div class="neon-card" style="margin-bottom:16px;">
# #                 <h4>{title}</h4>
# #                 <p style="color:#a0a6b1; white-space:pre-wrap;">{body}</p>
# #                 <p><strong>Premium:</strong> {is_premium}</p>
# #             </div>
# #             """,
# #             unsafe_allow_html=True,
# #         )

# # # import streamlit as st
# # # from math_saas.utils.db import get_supabase
# # # from math_saas.utils.formatter import fix_math_rendering  # ✅ new import
# # # from math_saas.subscriptions.core import get_active_subscription
# # # from math_saas.auth import TEXT_MUTED

# # # def render_public_content():
# # #     sb = get_supabase()
# # #     res = sb.table("public_content").select("*").order("created_at", desc=True).execute()
# # #     items = res.data or []

# # #     if not items:
# # #         st.info("No public content available.")
# # #         return

# # #     for item in items:
# # #         title = item.get("title", "Untitled")
# # #         body = item.get("body", "")
# # #         is_premium = item.get("is_premium", False)

# # #         # ✅ Auto‑fix math rendering before display
# # #         body = fix_math_rendering(body)

# # #         st.markdown(
# # #             f"""
# # #             <div class="neon-card" style="margin-bottom:16px;">
# # #                 <h4>{title}</h4>
# # #                 <p style="color:#a0a6b1; white-space:pre-wrap;">{body}</p>
# # #                 <p><strong>Premium:</strong> {is_premium}</p>
# # #             </div>
# # #             """,
# # #             unsafe_allow_html=True,
# # #         )

# # # # import streamlit as st
# # # # from math_saas.utils.db import get_supabase
# # # # from math_saas.subscriptions.core import get_active_subscription
# # # # from math_saas.auth import TEXT_MUTED


# # # # def render_public_content():
# # # #     st.markdown("<h3>Mathematical Concepts & Latest News</h3>", unsafe_allow_html=True)

# # # #     sb = get_supabase()

# # # #     # Fetch content
# # # #     try:
# # # #         res = sb.table("public_content").select("*").order("created_at", desc=True).execute()
# # # #         raw_items = res.data or []
# # # #     except Exception as e:
# # # #         st.error(f"Error fetching content: {e}")
# # # #         return

# # #     # # Debug: verify data fetched from Supabase
# # #     # debug_res = sb.table("public_content").select("title, created_at").execute()
# # #     # st.write("DEBUG:", debug_res.data)

# # #     # Only keep dict items
# # #     items = [i for i in raw_items if isinstance(i, dict)]

# # #     # Student session
# # #     student = st.session_state.get("student")
# # #     user_id = student["id"] if isinstance(student, dict) else None

# # #     # Subscription check
# # #     sub = get_active_subscription(user_id) if user_id else None
# # #     has_access = sub is not None

# # #     if not items:
# # #         st.info("No content available yet.")
# # #         return

# # #     for item in items:
# # #         title = item.get("title", "Untitled")
# # #         body = item.get("body", "")
# # #         premium = item.get("is_premium", False)

# # #         # Premium content but user not subscribed → teaser only
# # #         if premium and not has_access:
# # #             st.markdown(
# # #                 f"""
# # #                 <div class="neon-card" style="margin-bottom:12px;">
# # #                     <h4>{title}</h4>
# # #                     <p style="color:{TEXT_MUTED};">
# # #                         Premium content — subscribe to read more.
# # #                     </p>
# # #                 </div>
# # #                 """,
# # #                 unsafe_allow_html=True,
# # #             )
# # #             continue

# # #         # Full content
# # #         st.markdown(
# # #             f"""
# # #             <div class="neon-card" style="margin-bottom:12px;">
# # #                 <h4>{title}</h4>
# # #                 <p style="color:{TEXT_MUTED}; white-space:pre-wrap;">
# # #                     {body}
# # #                 </p>
# # #             </div>
# # #             """,
# # #             unsafe_allow_html=True,
# # #         )

# # # # import streamlit as st
# # # # from math_saas.utils.db import get_supabase
# # # # from math_saas.subscriptions.core import get_active_subscription
# # # # from math_saas.auth import TEXT_MUTED


# # # # def render_public_content():
# # # #     st.markdown("<h3>Mathematical Concepts & Latest News</h3>", unsafe_allow_html=True)

# # # #     sb = get_supabase()

# # # #     # Fetch content
# # # #     res = sb.table("public_content").select("*").order("created_at", desc=True).execute()
# # # #     raw_items = res.data or []

# # # #     # Only keep dict items
# # # #     items = [i for i in raw_items if isinstance(i, dict)]

# # # #     # Student session
# # # #     student = st.session_state.get("student")
# # # #     user_id = student["id"] if isinstance(student, dict) else None

# # # #     # Subscription check
# # # #     sub = get_active_subscription(user_id) if user_id else None
# # # #     has_access = sub is not None

# # # #     if not items:
# # # #         st.info("No content available yet.")
# # # #         return

# # # #     for item in items:
# # # #         # Safe key access
# # # #         title = item.get("title", "Untitled")
# # # #         body = item.get("body", "")
# # # #         premium = item.get("is_premium", False)

# # # #         # Premium content but user not subscribed → teaser only
# # # #         if premium and not has_access:
# # # #             st.markdown(
# # # #                 f"""
# # # #                 <div class="neon-card" style="margin-bottom:12px;">
# # # #                     <h4>{title}</h4>
# # # #                     <p style="color:{TEXT_MUTED};">
# # # #                         Premium content — subscribe to read more.
# # # #                     </p>
# # # #                 </div>
# # # #                 """,
# # # #                 unsafe_allow_html=True,
# # # #             )
# # # #             continue

# # # #         # Full content
# # # #         st.markdown(
# # # #             f"""
# # # #             <div class="neon-card" style="margin-bottom:12px;">
# # # #                 <h4>{title}</h4>
# # # #                 <p style="color:{TEXT_MUTED}; white-space:pre-wrap;">
# # # #                     {body}
# # # #                 </p>
# # # #             </div>
# # # #             """,
# # # #             unsafe_allow_html=True,
# # # #         )
