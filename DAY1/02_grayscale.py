import cv2
import os
import numpy as np

print("="*50)
print("OpenCV 範例 02: 轉換成灰階圖片")
print("="*50)

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
img_path = os.path.join(parent_dir, 'bright front and back', 'WIN_20250914_16_53_29_Pro.jpg')

print(f"\n讀取圖片: {os.path.basename(img_path)}")

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

    save_path = os.path.join(current_dir, 'grayscale_result.jpg')
    cv2.imwrite(save_path, gray)
    print(f"\n灰階圖片已儲存至: {os.path.basename(save_path)}")
    print("\n完成！")