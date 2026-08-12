import os
from supabase import create_client, Client

# ─── Config ────────────────────────────────────────────────────────────────────
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://aputhqpdygjiqqjkzjpg.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sb_publishable_jSVMnv37auvfYccscV7v8w_L60GjLBF")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)