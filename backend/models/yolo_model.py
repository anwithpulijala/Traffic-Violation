from ultralytics import YOLO
from pathlib import Path

# Load model from the models directory
model_path = Path(__file__).parent / "best.pt"
model = YOLO(str(model_path))
