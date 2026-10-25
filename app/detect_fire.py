# detect_fire.py
from ultralytics import YOLO
import os
import sys

# ------------------------------
# CONFIGURATION
# ------------------------------
MODEL_PATH = r"D:\PROJECTS\Vidya B-TECH\Fire and accident detection web\fire-smoke-detection.v2-v2.yolov8\runs\detect\fire_smoke_model3\weights\best.pt"
VIDEO_PATH = r"D:\PROJECTS\Vidya\Fire and accident detection web\Accident\acv.mp4"
OUTPUT_DIR = r"D:\PROJECTS\Vidya\Fire and accident detection web\project\media\results\fire_predictions"

# Ensure model exists
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")

# Ensure video exists
if not os.path.exists(VIDEO_PATH):
    raise FileNotFoundError(f"Video file not found at: {VIDEO_PATH}")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------------
# LOAD YOLO MODEL
# ------------------------------
print("🚀 Loading YOLO fire detection model...")
model = YOLO(MODEL_PATH)

# ------------------------------
# RUN PREDICTION
# ------------------------------
print(f"🎥 Running fire detection on video: {VIDEO_PATH}")

results = model.predict(
    source=VIDEO_PATH,
    save=True,
    project=OUTPUT_DIR,
    name="predictions",
    exist_ok=True,
    conf=0.3,
    imgsz=640
)

# ------------------------------
# CHECK RESULTS
# ------------------------------
if results:
    print("✅ Detection completed!")
    # Get path to latest saved video
    saved_videos = [f for f in os.listdir(os.path.join(OUTPUT_DIR, "predictions")) if f.lower().endswith((".mp4", ".avi"))]
    if saved_videos:
        latest_video = max(saved_videos, key=lambda f: os.path.getmtime(os.path.join(OUTPUT_DIR, "predictions", f)))
        latest_video_path = os.path.join(OUTPUT_DIR, "predictions", latest_video)
        print(f"📁 Result saved at: {latest_video_path}")
    else:
        print("⚠️ No output video found.")
else:
    print("⚠️ No results returned by the model.")

print("🎬 Fire detection script finished!")
