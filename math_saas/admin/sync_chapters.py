import streamlit as st
import requests
from supabase import create_client

def get_supabase():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["service_role_key"]
    return create_client(url, key)

def sync_chapters():
    sb = get_supabase()
    url = "https://jsdasr-math-cbse.vercel.app/9th-Math/index.html"
    html = requests.get(url).text  # noqa: F841

    chapters = [
        "Chapter 1 - Number Systems",
        "Chapter 2 - Polynomials",
        "Chapter 3 - Coordinate Geometry",
        "Chapter 4 - Linear Equations in Two Variables",
        "Chapter 5 - Introduction to Euclid's Geometry",
        "Chapter 6 - Lines and Angles",
        "Chapter 7 - Triangles",
        "Chapter 8 - Quadrilaterals",
        "Chapter 9 - Circles",
        "Chapter 10 - Heron's Formula",
        "Chapter 11 - Surface Areas and Volumes",
        "Chapter 12 - Statistics"
    ]

    for ch in chapters:
        sb.table("sync_chapters").insert({
            "grade": "9",
            "board": "CBSE",
            "chapter_title": ch,
            "description": f"{ch} imported from CBSE 9th Math portal.",
            "is_published": True
        }).execute()

if __name__ == "__main__":
    sync_chapters()
