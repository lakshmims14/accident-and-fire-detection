from ultralytics import YOLO

# Load YOLOv8 model (Nano version is fastest, use 'yolov8m.pt' or 'yolov8l.pt' for better accuracy)
model = YOLO('yolov8n.pt')  # You can also use yolov8s.pt, yolov8m.pt etc.

# Train the model
model.train(
    data='car_accident.yaml',  # path to your YAML file
    epochs=50,
    imgsz=640,
    batch=16,
    name='accident_detector'
)
