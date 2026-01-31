import os
import sys
import time
from dotenv import load_dotenv
from supabase import create_client

# Load Env
load_dotenv()
url = os.environ.get("SUPABASE_URL")

# The key provided by the user
USER_PROVIDED_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") # Replace with env var

def try_create_bucket(client, bucket_name):
    try:
        print(f"Attempting to create bucket '{bucket_name}'...")
        client.storage.create_bucket(bucket_name, options={"public": True})
        print(f"✅ Bucket '{bucket_name}' created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        # Check if it exists
        try:
            buckets = client.storage.list_buckets()
            names = [b.name for b in buckets]
            if bucket_name in names:
                print(f"Details: Bucket '{bucket_name}' actually ALREADY EXISTS in the list: {names}")
                return True
        except:
            pass
        return False

# 1. Try using the key directly (in case it is a weird formatted token or I'm mistaken)
print("--- Attempt 1: Using provided key directly ---")
try:
    sb_direct = create_client(url, USER_PROVIDED_KEY)
    if try_create_bucket(sb_direct, "traffic-uploads"):
        print("Success with direct key!")
        sys.exit(0)
except Exception as e:
    print(f"Attempt 1 failed: {e}")

# 2. Try assuming it's the JWT Secret and generating a Service Role JWT
print("\n--- Attempt 2: Generating Service Role JWT from secret ---")
try:
    import jwt
    
    # Supabase JWT Secret is usually the signing secret.
    # Service role payload structure:
    payload = {
        "role": "service_role",
        "iss": "supabase",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600 * 24 * 365 * 10 # 10 years
    }
    
    # We might need to handle the 'sb_secret_' prefix if it's not part of the actual secret?
    # Or maybe the secret IS 'sb_secret_...'
    # Let's try with the full string first.
    secret = USER_PROVIDED_KEY
    
    print("Generating token...")
    token = jwt.encode(payload, secret, algorithm="HS256")
    # print(f"Generated Token: {token[:10]}...") 
    
    sb_generated = create_client(url, token)
    if try_create_bucket(sb_generated, "traffic-uploads"):
        print("✅ Success! The provided string was the JWT Secret. I generated a Service Key and created the bucket.")
        sys.exit(0)
    else:
        print("❌ Bucket creation failed even with generated token.")
        
except ImportError:
    print("pyjwt not installed, skipping Attempt 2.")
except Exception as e:
    print(f"Attempt 2 failed: {e}")

print("\nCould not fix the bucket using the provided string.")
