

import cv2
import os

print("="*50)
print("OpenCV 範例 01: 讀取並顯示圖片")
print("="*50)

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
img_path = "D:\\AWORKSPACE\\Github\\ComputerVisioncourse\\DAY1\\bright front and back\\WIN_20250914_16_53_29_Pro.jpg"

print(f"\n讀取圖片: {os.path.basename(img_path)}")

img = cv2.imread(img_path)

if img is None:
    print("錯誤：無法讀取圖片！")
else:
    print(f"原始圖片尺寸: {img.shape[1]} x {img.shape[0]}")

    max_width = 800
    max_height = 600
    height, width = img.shape[:2]

    if width > max_width or height > max_height:
        scale = min(max_width/width, max_height/height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        img_resized = cv2.resize(img, (new_width, new_height))
        print(f"縮放後尺寸: {new_width} x {new_height}")
    else:
        img_resized = img
        print("圖片尺寸適中，不需縮放")

    cv2.imshow('Image', img_resized)
    print("\n按任意鍵關閉視窗...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("\n完成！")