import requests
import streamlit as st
from typing import List, Dict #Any ommitted
from supabase import create_client


# ---------------------------------------------------------
# SUPABASE CLIENT
# ---------------------------------------------------------
def get_supabase():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["service_role_key"]
    return create_client(url, key)


# ---------------------------------------------------------
# STATIC CHAPTER SOURCE (CAN BE EXTENDED LATER)
# ---------------------------------------------------------
def _get_cbse_9th_math_chapters() -> List[Dict[str, str]]:
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
        "Chapter 12 - Statistics",
    ]

    return [
        {
            "grade": "9",
            "board": "CBSE",
            "chapter_key": f"cbse9_{i+1}",
            "chapter_name": ch,
        }
        for i, ch in enumerate(chapters)
    ]


# ---------------------------------------------------------
# SYNC INTO MAIN CHAPTERS TABLE
# ---------------------------------------------------------
def sync_chapters():
    sb = get_supabase()

    # Optional: fetch HTML (future parsing)
    try:
        requests.get("https://jsdasr-math-cbse.vercel.app/9th-Math/index.html", timeout=10)
    except Exception:
        pass  # HTML not used yet, but kept for future scraping

    chapters = _get_cbse_9th_math_chapters()

    inserted = 0
    skipped = 0

    for ch in chapters:
        # Check if chapter already exists
        existing = (
            sb.table("chapters")
            .select("id")
            .eq("grade", ch["grade"])
            .eq("board", ch["board"])
            .eq("chapter_key", ch["chapter_key"])
            .execute()
            .data
        )

        if existing:
            skipped += 1
            continue

        try:
            sb.table("chapters").insert(ch).execute()
            inserted += 1
        except Exception as exc:
            st.error(f"Failed to insert chapter {ch['chapter_name']}: {exc}")

    st.success(f"Sync complete. Inserted: {inserted}, Skipped (already existed): {skipped}")


# ---------------------------------------------------------
# DIRECT RUN SUPPORT
# ---------------------------------------------------------
if __name__ == "__main__":
    sync_chapters()
