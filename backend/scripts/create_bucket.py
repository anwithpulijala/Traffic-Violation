import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("Error: Missing SUPABASE_URL or SUPABASE_KEY in .env")
    exit(1)

supabase = create_client(url, key)

bucket_name = "traffic-uploads"

try:
    print(f"Creating bucket '{bucket_name}'...")
    # Attempt to create the bucket (public=True is essential)
    supabase.storage.create_bucket(bucket_name, options={"public": True})
    print(f"Success: Bucket '{bucket_name}' created successfully!")
except Exception as e:
    # If it fails, it might be because it already exists or permissions issue
    print(f"Result: {e}")
    
    # List buckets to verify
    try:
        buckets = supabase.storage.list_buckets()
        print("Current Buckets:", [b.name for b in buckets])
    except Exception as list_err:
        print(f"Could not list buckets: {list_err}")
