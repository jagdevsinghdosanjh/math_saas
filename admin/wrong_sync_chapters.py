import requests
import streamlit as st
from typing import List, Dict
from supabase import create_client


# ---------------------------------------------------------
# SUPABASE CLIENT
# ---------------------------------------------------------
def get_supabase():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["service_role_key"]
    return create_client(url, key)


# ---------------------------------------------------------
# STATIC CHAPTER SOURCES
# ---------------------------------------------------------
def _get_cbse_9th_math_chapters() -> List[Dict[str, str]]:
    chapters = [
        "Chapter 1 - Number Systems(9th)",
        "Chapter 2 - Polynomials(9th)",
        "Chapter 3 - Coordinate Geometry(9th)",
        "Chapter 4 - Linear Equations in Two Variables(9th)",
        "Chapter 5 - Introduction to Euclid's Geometry(9th)",
        "Chapter 6 - Lines and Angles(9th)",
        "Chapter 7 - Triangles(9th)",
        "Chapter 8 - Quadrilaterals(9th)",
        "Chapter 9 - Circles(9th)",
        "Chapter 10 - Heron's Formula(9th)",
        "Chapter 11 - Surface Areas and Volumes(9th)",
        "Chapter 12 - Statistics(9th)",
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


def _get_cbse_10th_math_chapters() -> List[Dict[str, str]]:
    chapters = [
        "Chapter 1 - Real Numbers (10th)",
        "Chapter 2 - Polynomials(10th)",
        "Chapter 3 - Pair of Linear Equations in Two Variables(10th)",
        "Chapter 4 - Quadratic Equations(10th)",
        "Chapter 5 - Arithmetic Progression(10th)",
        "Chapter 6 - Coordinate Geometry(10th)",
        "Chapter 7 - Triangles(10th)",
        "Chapter 8 - Circles(10th)",
        "Chapter 9 - Introduction to Geometry(10th)",
        "Chapter 10 - Trigonometric Identities(10th)",
        "Chapter 11 - Heights and Distances: AOE & AOD(10th)",
        "Chapter 12 - Areas Related to Circles(10th)",
        "Chapter 13 - Surface Areas and Volumes(10th)",
        "Chapter 14 - Statistics(10th)",
        "Chapter 15 - Probability(10th)",
    ]

    return [
        {
            "grade": "10",
            "board": "CBSE",
            "chapter_key": f"cbse10_{i+1}",
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
        requests.get("https://jsdasr-math-cbse.vercel.app/10th-Math/index.html", timeout=10)
    except Exception:
        pass

    chapters = []
    chapters.extend(_get_cbse_9th_math_chapters())
    chapters.extend(_get_cbse_10th_math_chapters())

    inserted = 0
    skipped = 0

    for ch in chapters:
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
