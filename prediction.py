from ultralytics import YOLO

model = YOLO(r"D:\PROJECTS\Fire\fire-smoke-detection.v2-v2.yolov8\runs\detect\fire_smoke_model3\weights\best.pt")

metrics = model.val(
    data=r"D:\PROJECTS\Fire\fire-smoke-detection.v2-v2.yolov8\data.yaml",
    device='cpu'
)

print("\n📊 MODEL EVALUATION RESULTS 📊")
print(f"Precision: {metrics.box.map50:.4f}")     # Precision at IoU 0.50
print(f"Recall: {metrics.box.map75:.4f}")        # Recall at IoU 0.75
print(f"mAP@0.5: {metrics.box.map50:.4f}")       # mean Average Precision at IoU=0.5
print(f"mAP@0.5:0.95: {metrics.box.map:.4f}")    # mean Average Precision (0.5 to 0.95)

image_path = r"D:\PROJECTS\voice\new3.jpg"
results = model.predict(source=image_path, show=True, conf=0.25, device='cpu')

results[0].save(filename="prediction_result.jpg")

print("\n✅ Prediction complete! Result saved as 'prediction_result.jpg'")
