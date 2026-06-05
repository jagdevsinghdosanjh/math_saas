import streamlit as st
from math_saas.utils.db import supabase

def render():
    st.header("Chapters")

    sb = supabase()
    chapters = sb.table("chapters").select("*").order("id", desc=True).execute().data

    st.subheader("All Chapters")
    st.dataframe(chapters, use_container_width=True)

    st.subheader("Add Chapter")
    with st.form("add_chapter"):
        grade = st.text_input("Grade")
        board = st.text_input("Board")
        chapter_key = st.text_input("Chapter Key")
        chapter_name = st.text_input("Chapter Name")
        submit = st.form_submit_button("Create")

        if submit:
            sb.table("chapters").insert({
                "grade": grade,
                "board": board,
                "chapter_key": chapter_key,
                "chapter_name": chapter_name
            }).execute()
            st.success("Chapter added. Refresh to see changes.")

# import streamlit as st
# from math_saas.utils.db import get_supabase

# def render():
#     st.header("Chapters")

#     supabase = get_supabase()
#     res = (
#         supabase.table("chapters")
#         .select("*")
#         .order("created_at", desc=True)
#         .execute()
#     )
#     chapters = res.data or []

#     st.subheader("All Chapters")
#     st.dataframe(chapters, use_container_width=True)

#     st.subheader("Add Chapter")
#     with st.form("add_chapter"):
#         title = st.text_input("Title")
#         slug = st.text_input("Slug")
#         description = st.text_area("Description")
#         is_published = st.checkbox("Published", value=True)
#         submitted = st.form_submit_button("Create")
#         if submitted:
#             if not title or not slug:
#                 st.error("Title and slug are required.")
#             else:
#                 supabase.table("chapters").insert(
#                     {
#                         "title": title,
#                         "slug": slug,
#                         "description": description,
#                         "is_published": is_published,
#                     }
#                 ).execute()
#                 st.success("Chapter created. Refresh to see changes.")
