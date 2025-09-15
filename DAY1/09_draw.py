import cv2
import os
import numpy as np

print("="*50)
print("OpenCV 範例 09: 繪製形狀和文字")
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

    img_draw = img_resized.copy()

    cv2.rectangle(img_draw, (50, 50), (200, 150), (0, 255, 0), 3)
    cv2.rectangle(img_draw, (220, 50), (370, 150), (255, 0, 0), -1)

    cv2.circle(img_draw, (100, 250), 40, (255, 0, 0), 3)
    cv2.circle(img_draw, (200, 250), 40, (0, 0, 255), -1)

    cv2.line(img_draw, (50, 350), (550, 350), (255, 255, 0), 2)
    cv2.line(img_draw, (50, 370), (550, 370), (0, 255, 255), 5)

    pts = np.array([[400, 50], [450, 100], [430, 150], [370, 150], [350, 100]], np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(img_draw, [pts], True, (255, 0, 255), 3)

    cv2.ellipse(img_draw, (450, 250), (80, 40), 0, 0, 360, (128, 0, 128), 2)
    cv2.ellipse(img_draw, (450, 250), (40, 80), 0, 0, 180, (255, 128, 0), -1)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img_draw, 'OpenCV Demo', (50, 450), font, 1.5, (255, 255, 255), 3)

    font2 = cv2.FONT_HERSHEY_COMPLEX
    cv2.putText(img_draw, 'DAY1 Tutorial', (50, 500), font2, 1, (0, 255, 0), 2)

    font3 = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
    cv2.putText(img_draw, 'Computer Vision', (50, 550), font3, 0.8, (255, 255, 0), 2)

    cv2.imshow('Drawing Shapes and Text', img_draw)
    print(f"\n繪製內容說明:")
    print("矩形：")
    print("  - 綠色空心矩形 (thickness=3)")
    print("  - 藍色實心矩形 (thickness=-1)")
    print("\n圓形：")
    print("  - 藍色空心圓")
    print("  - 紅色實心圓")
    print("\n線條：")
    print("  - 黃色細線 (thickness=2)")
    print("  - 青色粗線 (thickness=5)")
    print("\n多邊形：")
    print("  - 紫色五邊形")
    print("\n橢圓：")
    print("  - 紫色橢圓框")
    print("  - 橘色半橢圓")
    print("\n文字：")
    print("  - 三種不同字體")
    print("\n按任意鍵關閉視窗...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    save_path = os.path.join(current_dir, 'drawing_result.jpg')
    cv2.imwrite(save_path, img_draw)
    print(f"\n繪製結果已儲存至: {os.path.basename(save_path)}")
    print("\n完成！")