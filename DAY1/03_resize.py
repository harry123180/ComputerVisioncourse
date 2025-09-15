import cv2
import os
import numpy as np

print("="*50)
print("OpenCV 範例 03: 調整圖片大小")
print("="*50)

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
img_path = os.path.join(parent_dir, 'bright front and back', 'WIN_20250914_16_53_29_Pro.jpg')

print(f"\n讀取圖片: {os.path.basename(img_path)}")

img = cv2.imread(img_path)

if img is None:
    print("錯誤：無法讀取圖片！")
else:
    height, width = img.shape[:2]
    print(f"原始尺寸: {width} x {height}")

    img_50 = cv2.resize(img, (width//2, height//2))
    img_25 = cv2.resize(img, (width//4, height//4))
    img_fixed = cv2.resize(img, (400, 300))

    max_display = 400
    scale = min(max_display/width, max_display/height)
    display_w = int(width * scale)
    display_h = int(height * scale)
    img_display = cv2.resize(img, (display_w, display_h))

    row1 = np.hstack([img_25, img_25])
    row2 = np.hstack([img_25, img_25])
    combined = np.vstack([row1, row2])

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(combined, '25%', (10, 30), font, 1, (0, 255, 0), 2)
    cv2.putText(combined, '25%', (img_25.shape[1]+10, 30), font, 1, (0, 255, 0), 2)

    cv2.imshow('Different Sizes (25% each)', combined)
    print(f"\n縮放比例展示:")
    print(f"25% 大小: {img_25.shape[1]} x {img_25.shape[0]}")
    print(f"50% 大小: {img_50.shape[1]} x {img_50.shape[0]}")
    print(f"固定大小: 400 x 300")
    print("\n按任意鍵關閉視窗...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    save_path = os.path.join(current_dir, 'resized_result.jpg')
    cv2.imwrite(save_path, img_fixed)
    print(f"\n調整後圖片已儲存至: {os.path.basename(save_path)}")
    print("\n完成！")