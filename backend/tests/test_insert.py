import sys
import os
sys.path.append(os.getcwd())
from app.services.supabase_service import SupabaseService
import datetime

print("Testing Supabase Insert...")

data = {
    "filename": "test_script_entry.png",
    "original_file_url": "http://example.com/orig",
    "processed_file_url": "http://example.com/proc",
    "helmet_detected": "TEST",
    "number_plate_detected": "TEST",
    "plate_number": "TEST-123"
}

try:
    response = SupabaseService.insert_record(data)
    print(f"Insert finished. Result: {response}")
except Exception as e:
    print(f"Insert failed: {e}")
