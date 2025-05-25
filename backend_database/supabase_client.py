from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="/app/.env")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("SUPABASE_URL:", SUPABASE_URL)
print("SUPABASE_KEY:", SUPABASE_KEY)
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL or Key is missing")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)