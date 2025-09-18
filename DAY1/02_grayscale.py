import cv2
import os
import numpy as np
img_path = "D:\\AWORKSPACE\\Github\\ComputerVisioncourse\\DAY1\\bright front and back\\WIN_20250914_16_53_29_Pro.jpg"
img = cv2.imread(img_path)
if img is None:
    print("錯誤：無法讀取圖片！")
else:
    max_width = 600
    height, width = img.shape[:2]
    scale = max_width / width
    new_width = int(width * scale)
    new_height = int(height * scale)
    img_resized = cv2.resize(img, (new_width, new_height))
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    combined = np.hstack([img_resized, cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)])
    cv2.imshow('Original vs Grayscale', combined)
    print(f"\n顯示尺寸: {new_width} x {new_height}")
    print("左邊：原始彩色圖片")
    print("右邊：灰階圖片")
    print("\n按任意鍵關閉視窗...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
