import cv2
import os
from models.yolo_model import model
import easyocr
import numpy as np

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

def process_video(video_path, filename):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Switch to WebM (VP80) for reliable browser playback
    out_path = os.path.join(OUTPUT_DIR, f"out_{filename}.webm")
    fourcc = cv2.VideoWriter_fourcc(*'vp80')
    out = cv2.VideoWriter(
        out_path,
        fourcc,
        fps,
        (w, h)
    )

    helmet_confirm_count = 0
    no_helmet_confirm_count = 0
    
    plate_detected = False
    plate_text = "N/A"
    
    frame_count = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames: {total_frames}")

    last_boxes = [] # Store (x1, y1, x2, y2, label, color)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        
        # Process every 5th frame
        if frame_count % 5 != 0:
            # Draw last known boxes on the current frame
            for (x1, y1, x2, y2, label, color) in last_boxes:
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            out.write(frame)
            continue

        print(f"Processing frame {frame_count}/{total_frames}")
        
        results = model(frame, conf=0.4)[0]

        current_frame_has_helmet = False
        current_frame_has_no_helmet = False

        for box, cls in zip(results.boxes.xyxy, results.boxes.cls):
            cls = int(cls)

            # Helmet logic
            if cls == 1:
                current_frame_has_no_helmet = True
            elif cls == 0:
                current_frame_has_helmet = True

            # Number plate detection
            if cls == 3:  # number plate
                plate_detected = True
                
                # Simple approach: If plate_text is N/A, try to find it.
                if plate_text == "N/A":
                    x1, y1, x2, y2 = map(int, box)
                    plate_img = frame[y1:y2, x1:x2]
                    try:
                        ocr_result = reader.readtext(plate_img)
                        detected_texts = [text[1] for text in ocr_result if text[2] > 0.3]
                        if detected_texts:
                            plate_text = " ".join(detected_texts).upper()
                    except:
                        pass

        # Update counters and store boxes for next frames
        last_boxes = []
        
        # We need to re-iterate or store during the first loop. 
        # Since we already iterated, let's just grab from results again or do it in the first loop.
        # Actually, let's construct last_boxes inside the previous loop to avoid double iteration?
        # But we need the color and label logic which is partly inside the loop (e.g. helmet logic)
        # Let's just do a quick pass or use the data we have.
        
        # Re-parsing results for storage
        for box, cls, conf in zip(results.boxes.xyxy, results.boxes.cls, results.boxes.conf):
            cls = int(cls)
            x1, y1, x2, y2 = map(int, box)
            label = f"{model.names[cls]} {conf:.2f}"
            color = (0, 255, 0) # Default Green

            if cls == 1: # No Helmet
                color = (0, 0, 255) # Red
            elif cls == 0: # Helmet
                color = (0, 255, 0) # Green
            elif cls == 3: # Number Plate
                color = (255, 0, 0) # Blue
            
            last_boxes.append((x1, y1, x2, y2, label, color))

        if current_frame_has_no_helmet:
            no_helmet_confirm_count += 1
        elif current_frame_has_helmet:
            helmet_confirm_count += 1

        out.write(results.plot())

    cap.release()
    out.release()
    
    # Decision logic based on majority/threshold
    # Prefer reporting violation if significant frames show no helmet
    if no_helmet_confirm_count > helmet_confirm_count:
        helmet_status = "NO"
    elif helmet_confirm_count > 0:
        helmet_status = "YES"
    else:
        helmet_status = "UNKNOWN"

    final_plate = "DETECTED" if plate_detected else "NOT DETECTED"

    return helmet_status, final_plate, out_path, plate_text
