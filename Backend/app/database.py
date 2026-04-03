from supabase import create_client, Client
from app.config import get_settings


def get_supabase() -> Client:
    """Public client (anon key) — respects RLS."""
    s = get_settings()
    return create_client(s.supabase_url, s.supabase_anon_key)


def get_supabase_admin() -> Client:
    """Service-role client — bypasses RLS. Use for server-side operations only."""
    s = get_settings()
    return create_client(s.supabase_url, s.supabase_service_role_key)
