import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("Error: Missing SUPABASE_URL or SUPABASE_KEY in .env")
    exit(1)

try:
    print(f"Connecting to {url}...")
    supabase = create_client(url, key)
    
    # Try to fetch 1 row from detections table to check permission/existence
    # We use .select("id").limit(1).execute() which is a lightweight check
    response = supabase.table("detections").select("id").limit(1).execute()
    
    print("✅ SUCCESS: Connected to Supabase Database!")
    print(f"Table 'detections' access confirmed. Data: {response.data}")

except Exception as e:
    print("❌ FAILED: Could not connect or query table.")
    print(f"Error Type: {type(e)}")
    print(f"Error Message: {e}")
