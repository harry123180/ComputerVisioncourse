from ultralytics import YOLO
import cv2

# 最簡單的版本
model_path = r"D:\AWORKSPACE\Github\ComputerVisioncourse\runs\train\yolov11_gpu\weights\best.pt"
model = YOLO(model_path)

# 直接使用predict串流模式
results = model.predict(source=0, show=True, conf=0.5)

# 或使用更簡潔的方式
for result in model.predict(source=0, stream=True, show=True):
    # 按ESC結束
    if cv2.waitKey(1) == 27:
        break