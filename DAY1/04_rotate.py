import cv2
import os
import numpy as np

print("="*50)
print("OpenCV 範例 04: 旋轉圖片")
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

    center = (new_width // 2, new_height // 2)

    rotate_45 = cv2.getRotationMatrix2D(center, 45, 1.0)
    img_45 = cv2.warpAffine(img_resized, rotate_45, (new_width, new_height))

    rotate_90 = cv2.getRotationMatrix2D(center, 90, 1.0)
    img_90 = cv2.warpAffine(img_resized, rotate_90, (new_width, new_height))

    rotate_180 = cv2.getRotationMatrix2D(center, 180, 1.0)
    img_180 = cv2.warpAffine(img_resized, rotate_180, (new_width, new_height))

    row1 = np.hstack([img_resized, img_45])
    row2 = np.hstack([img_90, img_180])
    combined = np.vstack([row1, row2])

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(combined, 'Original', (10, 30), font, 0.7, (0, 255, 0), 2)
    cv2.putText(combined, '45 deg', (new_width+10, 30), font, 0.7, (0, 255, 0), 2)
    cv2.putText(combined, '90 deg', (10, new_height+30), font, 0.7, (0, 255, 0), 2)
    cv2.putText(combined, '180 deg', (new_width+10, new_height+30), font, 0.7, (0, 255, 0), 2)

    cv2.imshow('Rotation Examples', combined)
    print(f"\n旋轉展示:")
    print("左上：原始圖片")
    print("右上：旋轉 45 度")
    print("左下：旋轉 90 度")
    print("右下：旋轉 180 度")
    print("\n按任意鍵關閉視窗...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    save_path = os.path.join(current_dir, 'rotated_result.jpg')
    cv2.imwrite(save_path, img_90)
    print(f"\n旋轉90度圖片已儲存至: {os.path.basename(save_path)}")
    print("\n完成！")