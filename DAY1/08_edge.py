import cv2
import os
import numpy as np

print("="*50)
print("OpenCV 範例 08: 邊緣檢測")
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

    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

    edges_canny = cv2.Canny(gray, 50, 150)

    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    sobel_combined = np.sqrt(sobel_x**2 + sobel_y**2)
    sobel_combined = np.uint8(np.clip(sobel_combined, 0, 255))

    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    laplacian = np.uint8(np.absolute(laplacian))

    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    edges_canny_blur = cv2.Canny(blur, 50, 150)

    row1 = np.hstack([gray, edges_canny])
    row2 = np.hstack([sobel_combined, laplacian])
    combined = np.vstack([row1, row2])

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(combined, 'Grayscale', (10, 30), font, 0.7, (255, 255, 255), 2)
    cv2.putText(combined, 'Canny', (new_width+10, 30), font, 0.7, (255, 255, 255), 2)
    cv2.putText(combined, 'Sobel', (10, new_height+30), font, 0.7, (255, 255, 255), 2)
    cv2.putText(combined, 'Laplacian', (new_width+10, new_height+30), font, 0.7, (255, 255, 255), 2)

    cv2.imshow('Edge Detection', combined)
    print(f"\n邊緣檢測展示:")
    print("左上：灰階原圖")
    print("右上：Canny 邊緣檢測 (最常用)")
    print("左下：Sobel 邊緣檢測 (梯度法)")
    print("右下：Laplacian 邊緣檢測 (二階微分)")
    print("\nCanny 參數: 低閾值=50, 高閾值=150")
    print("建議：先模糊再做邊緣檢測效果更好")
    print("\n按任意鍵關閉視窗...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    save_path = os.path.join(current_dir, 'edge_result.jpg')
    cv2.imwrite(save_path, edges_canny)
    print(f"\nCanny邊緣檢測結果已儲存至: {os.path.basename(save_path)}")
    print("\n完成！")