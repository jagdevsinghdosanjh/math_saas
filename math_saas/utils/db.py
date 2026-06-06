from supabase import create_client
from math_saas.config import SUPABASE_URL, SUPABASE_ANON_KEY

# Singleton client
_supabase = None


def get_supabase():
    """Return a singleton Supabase client."""

    # Pylance-safe checks
    if SUPABASE_URL is None:
        raise RuntimeError("SUPABASE_URL is not set in environment variables")

    if SUPABASE_ANON_KEY is None:
        raise RuntimeError("SUPABASE_ANON_KEY is not set in environment variables")

    global _supabase
    if _supabase is None:
        _supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

    return _supabase
