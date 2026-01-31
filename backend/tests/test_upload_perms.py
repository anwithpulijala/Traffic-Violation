import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.environ.get("SUPABASE_URL")
anon_key = os.environ.get("SUPABASE_KEY")
# Using the key provided by the user in chat history
service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

# Test Payload
file_name = "test_upload_debug.txt"
file_content = b"Debug upload content"
bucket = "traffic-uploads"

def test_upload(key_type, key):
    print(f"\n--- Testing upload with {key_type} key ---")
    try:
        # Re-init client with specific key
        client = create_client(url, key)
        
        # Try upload
        res = client.storage.from_(bucket).upload(
            path=file_name,
            file=file_content,
            file_options={"content-type": "text/plain", "upsert": "true"}
        )
        print(f"✅ Success! Response: {res}")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

# 1. Test Anon Key (Expected to fail if RLS is missing)
test_upload("ANON", anon_key)

# 2. Test Service Role Key (Expected to succeed)
# Note: Since I don't have the full JWT logic here easily without checking if the secret works as a key directly (it did for bucket creation),
# I'll try using the secret string directly as I did in fix_bucket.py.
test_upload("SERVICE_ROLE", service_key)
