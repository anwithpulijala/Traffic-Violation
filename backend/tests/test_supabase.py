import os
from dotenv import load_dotenv
from supabase import create_client

# Explicitly load .env from the same directory
load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

print(f"URL: {url}")
print(f"Key found: {'Yes' if key else 'No'}")

if not url or not key:
    print("Missing credentials.")
    exit(1)

try:
    supabase = create_client(url, key)
    print("Client initialized successfully.")
    
    # 1. Test Storage
    print("\n--- Testing Storage ---")
    try:
        buckets = supabase.storage.list_buckets()
        print(f"Buckets found: {[b.name for b in buckets]}")
        
        target_bucket = "traffic-uploads"
        if any(b.name == target_bucket for b in buckets):
            print(f"✅ Bucket '{target_bucket}' exists.")
        else:
            print(f"❌ Bucket '{target_bucket}' NOT found.")
    except Exception as e:
        print(f"Storage Error: {e}")

    # 2. Test Database
    print("\n--- Testing Database ---")
    try:
        # Try to select from detections (limit 1) just to check existence/access
        response = supabase.table("detections").select("*").limit(1).execute()
        print(f"✅ Table 'detections' access successful.")
        print(f"Data sample: {response.data}")
    except Exception as e:
        print(f"❌ Database Error (Table 'detections' might be missing or RLS blocking): {e}")

except Exception as e:
    print(f"Critical Connection Error: {e}")
