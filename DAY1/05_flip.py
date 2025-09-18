import cv2
import os
import numpy as np

print("="*50)
print("OpenCV 範例 05: 翻轉圖片")
print("="*50)

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
img_path = "D:\\AWORKSPACE\\Github\\ComputerVisioncourse\\DAY1\\bright front and back\\WIN_20250914_16_53_29_Pro.jpg"
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

    flip_horizontal = cv2.flip(img_resized, 1)
    flip_vertical = cv2.flip(img_resized, 0)
    flip_both = cv2.flip(img_resized, -1)

    row1 = np.hstack([img_resized, flip_horizontal])
    row2 = np.hstack([flip_vertical, flip_both])
    combined = np.vstack([row1, row2])

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(combined, 'Original', (10, 30), font, 0.7, (0, 255, 0), 2)
    cv2.putText(combined, 'Horizontal', (new_width+10, 30), font, 0.7, (0, 255, 0), 2)
    cv2.putText(combined, 'Vertical', (10, new_height+30), font, 0.7, (0, 255, 0), 2)
    cv2.putText(combined, 'Both', (new_width+10, new_height+30), font, 0.7, (0, 255, 0), 2)

    cv2.imshow('Flip Examples', combined)
    print(f"\n翻轉展示:")
    print("左上：原始圖片")
    print("右上：水平翻轉（左右鏡像）")
    print("左下：垂直翻轉（上下顛倒）")
    print("右下：水平+垂直翻轉")
    print("\n翻轉參數說明:")
    print("1 = 水平翻轉")
    print("0 = 垂直翻轉")
    print("-1 = 兩者都翻轉")
    print("\n按任意鍵關閉視窗...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    save_path = os.path.join(current_dir, 'flipped_result.jpg')
    cv2.imwrite(save_path, flip_horizontal)
    print(f"\n水平翻轉圖片已儲存至: {os.path.basename(save_path)}")
    print("\n完成！")