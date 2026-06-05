from supabase import create_client
from math_saas.config import SUPABASE_URL, SUPABASE_ANON_KEY

_supabase = None

def supabase():
    global _supabase
    if _supabase is None:
        _supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    return _supabase

# # Placeholder for future Supabase or SQL integration

# from supabase import create_client, Client
# from math_saas.config import SUPABASE_URL, SUPABASE_ANON_KEY

# _supabase: Client | None = None

# def get_supabase() -> Client:
#     global _supabase
#     if _supabase is None:
#         if not SUPABASE_URL or not SUPABASE_ANON_KEY:
#             raise RuntimeError("Supabase URL or ANON key not configured")
#         _supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
#     return _supabase
