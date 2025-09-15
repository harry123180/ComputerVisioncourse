import cv2
import os
import numpy as np

print("="*50)
print("OpenCV 範例 06: 調整亮度與對比度")
print("="*50)

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
img_path = os.path.join(parent_dir, 'bright front and back', 'WIN_20250914_16_53_29_Pro.jpg')

print(f"\n讀取圖片: {os.path.basename(img_path)}")

img = cv2.imread(img_path)

if img is None:
    print("錯誤：無法讀取圖片！")
else:
    max_width = 400
    height, width = img.shape[:2]
    scale = max_width / width
    new_width = int(width * scale)
    new_height = int(height * scale)
    img_resized = cv2.resize(img, (new_width, new_height))

    brighter = cv2.convertScaleAbs(img_resized, alpha=1.0, beta=50)
    darker = cv2.convertScaleAbs(img_resized, alpha=1.0, beta=-50)
    high_contrast = cv2.convertScaleAbs(img_resized, alpha=1.5, beta=0)
    low_contrast = cv2.convertScaleAbs(img_resized, alpha=0.5, beta=0)

    row1 = np.hstack([img_resized, brighter])
    row2 = np.hstack([darker, high_contrast])
    combined = np.vstack([row1, row2])

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(combined, 'Original', (10, 30), font, 0.7, (0, 255, 0), 2)
    cv2.putText(combined, 'Brighter +50', (new_width+10, 30), font, 0.7, (0, 255, 0), 2)
    cv2.putText(combined, 'Darker -50', (10, new_height+30), font, 0.7, (0, 255, 0), 2)
    cv2.putText(combined, 'Contrast x1.5', (new_width+10, new_height+30), font, 0.7, (0, 255, 0), 2)

    cv2.imshow('Brightness & Contrast', combined)
    print(f"\n亮度與對比度調整:")
    print("左上：原始圖片")
    print("右上：增加亮度 (+50)")
    print("左下：降低亮度 (-50)")
    print("右下：增加對比度 (x1.5)")
    print("\n公式: output = alpha * input + beta")
    print("alpha = 對比度係數 (1.0 = 不變)")
    print("beta = 亮度調整值 (0 = 不變)")
    print("\n按任意鍵關閉視窗...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    save_path = os.path.join(current_dir, 'brightness_result.jpg')
    cv2.imwrite(save_path, brighter)
    print(f"\n調亮圖片已儲存至: {os.path.basename(save_path)}")
    print("\n完成！")