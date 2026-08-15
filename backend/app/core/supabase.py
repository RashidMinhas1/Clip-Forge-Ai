from supabase import create_client, Client
from app.core.config import settings

def get_supabase_client() -> Client:
    """
    Returns a Supabase client initialized with the SERVICE ROLE KEY.
    WARNING: This client bypasses RLS. Use ONLY for privileged server-side operations
    or when manually enforcing security.
    """
    url: str = settings.NEXT_PUBLIC_SUPABASE_URL
    key: str = settings.SUPABASE_SERVICE_ROLE_KEY
    return create_client(url, key)
