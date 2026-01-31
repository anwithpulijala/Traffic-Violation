import cv2
import os
from models.yolo_model import model
import easyocr
import numpy as np

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_image(image_path, filename):
    img = cv2.imread(image_path)
    results = model(img, conf=0.4)[0]

    helmet_status = "UNKNOWN"
    plate_detected = False
    plate_text = "NOT DETECTED"

    for box, cls in zip(results.boxes.xyxy, results.boxes.cls):
        cls = int(cls)

        # Helmet logic
        if cls == 1:  # no_helmet
            helmet_status = "NO"
        elif cls == 0 and helmet_status != "NO":  # helmet
            helmet_status = "YES"

        # Number plate detection
        if cls == 3:  # number plate
            plate_detected = True
            
            # Extract coordinates
            x1, y1, x2, y2 = map(int, box)
            
            # Crop the number plate
            plate_img = img[y1:y2, x1:x2]
            
            # Perform OCR
            try:
                ocr_result = reader.readtext(plate_img)
                # Filter for high confidence and combine text
                detected_texts = [text[1] for text in ocr_result if text[2] > 0.3]
                if detected_texts:
                    plate_text = " ".join(detected_texts).upper()
            except Exception as e:
                print(f"OCR Error: {e}")

    # Save output image
    output_path = os.path.join(OUTPUT_DIR, f"out_{filename}")
    cv2.imwrite(output_path, results.plot())

    final_plate = "DETECTED" if plate_detected else "NOT DETECTED"

    return helmet_status, final_plate, output_path, plate_text
