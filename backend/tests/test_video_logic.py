import sys
import os
sys.path.append(os.getcwd())

from app.services.video_service import process_video

print("Testing process_video...")
try:
    # process_video returns: helmet_status, final_plate, out_path, plate_text
    result = process_video("dummy_video.mp4", "dummy_video.mp4")
    print(f"Success! Result: {result}")
except Exception as e:
    print(f"Failed: {e}")
    import traceback
    traceback.print_exc()
