import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.environ.get("DATABASE_URL")

print(f"DB URL found: {'Yes' if db_url else 'No'}")

try:
    print("Attempting to connect...")
    conn = psycopg2.connect(db_url)
    print("✅ Connected successfully to Supabase!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
