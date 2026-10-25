from ultralytics import YOLO
import os

MODEL_PATH = r"D:\PROJECTS\Vidya B-TECH\Fire and accident detection web\Accident\runs\detect\accident_detector\weights\best.pt"

VIDEO_PATH = r"D:\PROJECTS\Vidya\Fire and accident detection web\Accident\acv.mp4"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")

if not os.path.exists(VIDEO_PATH):
    raise FileNotFoundError(f"Video file not found at: {VIDEO_PATH}")

# Load YOLO model
print("🚀 Loading YOLO model...")
model = YOLO(MODEL_PATH)

# Run prediction
print("🎥 Detecting accidents...")
results = model.predict(
    source=VIDEO_PATH,
    save=True,
    conf=0.3,
    imgsz=640
)

print("✅ Detection completed!")
