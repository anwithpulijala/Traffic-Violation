import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = None

if url and key:
    try:
        supabase = create_client(url, key)
    except Exception as e:
        print(f"Failed to initialize Supabase client: {e}")
else:
    print("Warning: SUPABASE_URL or SUPABASE_KEY not found in environment variables. Supabase integration disabled.")

class SupabaseService:
    @staticmethod
    def upload_file(file_bytes: bytes, file_path: str, content_type: str = "image/png") -> str:
        """
        Uploads a file to Supabase Storage and returns the public URL.
        """
        if not supabase:
            print("Supabase client not initialized.")
            return None
        
        try:
            bucket_name = "traffic-uploads"
            # Remove leading slash if present
            if file_path.startswith("/"):
                file_path = file_path[1:]
            
            print(f"Attempting to upload to {bucket_name}/{file_path} with type {content_type}")
                
            response = supabase.storage.from_(bucket_name).upload(
                file=file_bytes,
                path=file_path,
                file_options={"content-type": content_type, "upsert": "true"}
            )
            print(f"Upload response: {response}")
            
            # Construct public URL
            public_url = f"{url}/storage/v1/object/public/{bucket_name}/{file_path}"
            print(f"Generated Public URL: {public_url}")
            return public_url
            
        except Exception as e:
            print(f"Supabase Upload Error for {file_path}: {e}")
            import traceback
            traceback.print_exc()
            return None

    @staticmethod
    def insert_record(data: dict):
        """
        Inserts a detection record into the 'detections' table.
        """
        if not supabase:
            print("Supabase client not initialized during insert.")
            return None
        
        try:
            print(f"Attempting to insert record: {data}")
            response = supabase.table("detections").insert(data).execute()
            print(f"Insert response: {response}")
            return response
        except Exception as e:
            print(f"Supabase Insert Error: {e}")
            import traceback
            traceback.print_exc()
            return None
