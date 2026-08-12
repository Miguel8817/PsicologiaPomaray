import os
from supabase import create_client, Client

# ─── Config ────────────────────────────────────────────────────────────────────
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://vjxdlsriootkyuuctgvl.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sb_publishable_W9Hzu7tPoqCtjxPMcA3k8g_69enusCm")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)