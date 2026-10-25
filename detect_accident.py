from ultralytics import YOLO
import sys

# Load trained model
model = YOLO(r'D:\PROJECTS\Fire and person detection\project\Accident\runs\detect\accident_detector\weights\best.pt')

# Predict from image
# model.predict(
#     source='/Users/shijojohn/PycharmProjects/Accident/custom_dataset/images/val/test4_41.jpg',  # or a folder, or a video file
#     save=True,
#     conf=0.3,
#     imgsz=640,
# )

# For video detection (e.g., from webcam or file)
# model.predict(source=0)  # for webcam
model.predict(source=r'D:\PROJECTS\Fire and person detection\project\Accident\acv.mp4', save=True)
