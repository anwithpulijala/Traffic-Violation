from fastapi import APIRouter, UploadFile, File
import os
import shutil

from app.services.image_service import process_image
from app.services.video_service import process_video

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

from typing import List

from fastapi import APIRouter, UploadFile, File, BackgroundTasks

# ... imports ...

@router.post("/detect")
def detect(background_tasks: BackgroundTasks, files: List[UploadFile] = File(...)):
    results = []
    
    for file in files:
        print(f"Received file: {file.filename}")
        try:
            filename = file.filename
            ext = filename.split('.')[-1].lower()
            file_path = os.path.join(UPLOAD_DIR, filename)

            # Reset file cursor before reading/copying if needed, though usually fresh UploadFile is at 0
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            image_exts = ["jpg", "jpeg", "png", "webp"]
            video_exts = ["mp4", "avi", "mov", "mkv"]
            
            # Determine file type and process
            if ext in image_exts:
                helmet, plate, output, plate_number = process_image(file_path, filename)
            elif ext in video_exts:
                helmet, plate, output, plate_number = process_video(file_path, filename)
            else:
                output = None
                helmet = "UNKNOWN"
                plate = "UNKNOWN"
                plate_number = "N/A"

            # Background Task for Supabase Ops
            background_tasks.add_task(handle_supabase_upload, 
                file_path, filename, ext, 
                output, helmet, plate, plate_number, image_exts
            )

            results.append({
                "filename": filename,
                "helmet": helmet,
                "number_plate": plate,
                "plate_number": plate_number,
                "output_file": output # Return local path for immediate display
            })
            
        except Exception as e:
            print(f"Error processing file {file.filename}: {e}")
            import traceback
            traceback.print_exc()
            results.append({"filename": file.filename, "error": str(e)})

    print("All processing complete")
    return results

def handle_supabase_upload(file_path, filename, ext, output, helmet, plate, plate_number, image_exts):
    from app.services.supabase_service import SupabaseService
    original_url = None
    processed_url = None
    
    # Upload Original
    try:
        with open(file_path, "rb") as f:
            file_bytes = f.read()
        original_url = SupabaseService.upload_file(file_bytes, f"originals/{filename}", f"image/{ext}" if ext in image_exts else f"video/{ext}")
    except Exception as e:
        print(f"Background Upload Error (Original): {e}")

    # Upload Processed
    if output and os.path.exists(output):
        try:
            with open(output, "rb") as f:
                out_bytes = f.read()
            
            out_ext = output.split('.')[-1].lower()
            mime_type = "video/webm" if out_ext == "webm" else (f"image/{out_ext}" if out_ext in image_exts else "application/octet-stream")
            
            processed_filename = os.path.basename(output)
            processed_url = SupabaseService.upload_file(out_bytes, f"processed/{processed_filename}", mime_type)
        except Exception as e:
            print(f"Background Upload Error (Processed): {e}")

    # Persist to DB
    if original_url and processed_url:
            SupabaseService.insert_record({
                "filename": filename,
                "original_file_url": original_url,
                "processed_file_url": processed_url,
                "helmet_detected": helmet,
                "number_plate_detected": plate,
                "plate_number": plate_number
            })
            print(f"Supabase record saved for {filename}")
