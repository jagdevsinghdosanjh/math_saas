import streamlit as st
from typing import List, Dict, Any
from supabase import create_client


# ---------------------------------------------------------
# TYPE ALIAS (Pylance‑safe JSON dict)
# ---------------------------------------------------------
SyncChapter = Dict[str, Any]


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
def _get_cbse_9th_math_chapters() -> List[SyncChapter]:
    chapter_titles = [
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
            "chapter_title": title,
            "chapter_url": None,
            "description": None,
            "is_published": False,
        }
        for title in chapter_titles
    ]


def _get_cbse_10th_math_chapters() -> List[SyncChapter]:
    chapter_titles = [
        "Chapter 1 - Real Numbers",
        "Chapter 2 - Polynomials",
        "Chapter 3 - Pair of Linear Equations in Two Variables",
        "Chapter 4 - Quadratic Equations",
        "Chapter 5 - Arithmetic Progression",
        "Chapter 6 - Coordinate Geometry",
        "Chapter 7 - Triangles",
        "Chapter 8 - Circles",
        "Chapter 9 - Introduction to Geometry",
        "Chapter 10 - Trigonometric Identities",
        "Chapter 11 - Heights and Distances: AOE & AOD",
        "Chapter 12 - Areas Related to Circles",
        "Chapter 13 - Surface Areas and Volumes",
        "Chapter 14 - Statistics",
        "Chapter 15 - Probability",
    ]

    return [
        {
            "grade": "10",
            "board": "CBSE",
            "chapter_title": title,
            "chapter_url": None,
            "description": None,
            "is_published": False,
        }
        for title in chapter_titles
    ]


# ---------------------------------------------------------
# SYNC INTO sync_chapters TABLE
# ---------------------------------------------------------
def sync_chapters() -> None:
    sb = get_supabase()

    chapters: List[SyncChapter] = []
    chapters.extend(_get_cbse_9th_math_chapters())
    chapters.extend(_get_cbse_10th_math_chapters())

    inserted = 0
    skipped = 0

    for ch in chapters:
        existing = (
            sb.table("sync_chapters")
            .select("id")
            .eq("grade", ch["grade"])
            .eq("board", ch["board"])
            .eq("chapter_title", ch["chapter_title"])
            .execute()
            .data
        )

        if existing:
            skipped += 1
            continue

        # dict(ch) ensures Pylance sees a JSON‑serializable dict
        sb.table("sync_chapters").insert(dict(ch)).execute()
        inserted += 1

    st.success(f"Sync complete. Inserted: {inserted}, Skipped: {skipped}")


if __name__ == "__main__":
    sync_chapters()
