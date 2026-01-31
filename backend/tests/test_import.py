import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    import app
    print("Import 'app' success")
    from app.services import supabase_service
    print("Import 'app.services.supabase_service' success")
except Exception as e:
    print(f"Error: {e}")
