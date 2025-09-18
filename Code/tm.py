import os
import sys
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
import cv2
import numpy as np

# 路徑
MODEL = r"D:\AWORKSPACE\Github\ComputerVisioncourse\Code\keras_model.h5"
LABELS = r"D:\AWORKSPACE\Github\ComputerVisioncourse\Code\labels.txt"

# 檢查檔案
if not all(os.path.exists(f) for f in [MODEL, LABELS]):
    print("找不到模型或標籤檔案")
    sys.exit(1)

# 修正 DepthwiseConv2D 相容性
class FixedDepthwiseConv2D(tf.keras.layers.DepthwiseConv2D):
    def __init__(self, **kwargs):
        kwargs.pop('groups', None)
        super().__init__(**kwargs)

# 載入模型和標籤
model = tf.keras.models.load_model(
    MODEL, 
    custom_objects={'DepthwiseConv2D': FixedDepthwiseConv2D},
    compile=False
)

with open(LABELS, 'r', encoding='utf-8') as f:
    labels = [line.strip().split(' ', 1)[-1] for line in f]

# 攝影機
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("無法開啟攝影機")
    sys.exit(1)

print("按 ESC 退出")

# 主迴圈
while True:
    ret, frame = cap.read()
    if not ret:
        continue
    
    cv2.imshow("Webcam", frame)
    
    # 預處理
    img = cv2.resize(frame, (224, 224))
    img = (img.astype(np.float32) / 127.5) - 1
    img = np.expand_dims(img, axis=0)
    
    # 預測
    pred = model.predict(img, verbose=0)[0]
    idx = np.argmax(pred)
    
    print(f"\r{labels[idx]}: {int(pred[idx]*100)}%", end="")
    
    if cv2.waitKey(1) == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()