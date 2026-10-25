from ultralytics import YOLO

# Load a pre-trained YOLOv8 model
model = YOLO("yolov8n.pt")

# Train using CPU
results = model.train(
    data=r"D:\PROJECTS\Fire\fire-smoke-detection.v2-v2.yolov8\data.yaml",
    epochs=50,
    imgsz=640,
    batch=5,               
    name="fire_smoke_model",
    device='cpu'           
)

print("✅ Training complete! Results saved in 'runs/detect/fire_smoke_model'")
