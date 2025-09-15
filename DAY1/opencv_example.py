import cv2
import numpy as np
import os
import sys

print("="*50)
print("OpenCV 範例程式")
print("="*50)

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
img_path = os.path.join(parent_dir, 'bright front and back', 'WIN_20250914_16_53_29_Pro.jpg')

print(f"\n當前腳本位置: {current_dir}")
print(f"專案根目錄: {parent_dir}")
print(f"圖片完整路徑: {img_path}")
print(f"圖片是否存在: {os.path.exists(img_path)}")

img = cv2.imread(img_path)

if img is None:
    print("錯誤：無法讀取圖片！")
    print("請確認圖片路徑是否正確")
else:
    print("圖片讀取成功！")
    print(f"圖片尺寸: {img.shape}")
    print(f"高度: {img.shape[0]} pixels")
    print(f"寬度: {img.shape[1]} pixels")
    print(f"通道數: {img.shape[2]}")
    print(f"資料類型: {img.dtype}")

    print("\n1. 顯示原始圖片")
    print("-"*30)
    cv2.imshow('Original Image', img)
    print("按任意鍵繼續...")
    cv2.waitKey(0)

    print("\n2. 轉換成灰階圖片")
    print("-"*30)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Grayscale Image', gray)
    print(f"灰階圖片尺寸: {gray.shape}")
    print("按任意鍵繼續...")
    cv2.waitKey(0)

    print("\n3. 調整圖片大小")
    print("-"*30)
    scale_percent = 50
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    print(f"縮小到 {scale_percent}% 大小")
    print(f"新尺寸: {resized.shape}")
    cv2.imshow('Resized Image (50%)', resized)
    print("按任意鍵繼續...")
    cv2.waitKey(0)

    print("\n4. 圖片旋轉")
    print("-"*30)
    center = (img.shape[1]//2, img.shape[0]//2)
    angle = 45
    scale = 0.5
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(img, rotation_matrix, (img.shape[1], img.shape[0]))
    print(f"旋轉 {angle} 度，縮放 {scale} 倍")
    cv2.imshow('Rotated Image (45 degrees)', rotated)
    print("按任意鍵繼續...")
    cv2.waitKey(0)

    print("\n5. 圖片翻轉")
    print("-"*30)
    flipped_h = cv2.flip(img, 1)
    flipped_v = cv2.flip(img, 0)
    flipped_both = cv2.flip(img, -1)

    h_concat1 = np.hstack([cv2.resize(img, (300, 200)),
                           cv2.resize(flipped_h, (300, 200))])
    h_concat2 = np.hstack([cv2.resize(flipped_v, (300, 200)),
                           cv2.resize(flipped_both, (300, 200))])
    v_concat = np.vstack([h_concat1, h_concat2])

    cv2.imshow('Flipped Images (Original, H-Flip, V-Flip, Both)', v_concat)
    print("顯示: 原圖 | 水平翻轉")
    print("      垂直翻轉 | 兩者都翻")
    print("按任意鍵繼續...")
    cv2.waitKey(0)

    print("\n6. 調整亮度和對比度")
    print("-"*30)
    alpha = 1.5
    beta = 30
    adjusted = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    print(f"對比度係數: {alpha}")
    print(f"亮度增加: {beta}")
    cv2.imshow('Brightness and Contrast Adjusted', adjusted)
    print("按任意鍵繼續...")
    cv2.waitKey(0)

    print("\n7. 模糊效果")
    print("-"*30)
    blur_avg = cv2.blur(img, (15, 15))
    blur_gaussian = cv2.GaussianBlur(img, (15, 15), 0)
    blur_median = cv2.medianBlur(img, 15)

    blur_compare = np.hstack([cv2.resize(img, (250, 170)),
                              cv2.resize(blur_avg, (250, 170)),
                              cv2.resize(blur_gaussian, (250, 170)),
                              cv2.resize(blur_median, (250, 170))])
    cv2.imshow('Blur Effects (Original, Average, Gaussian, Median)', blur_compare)
    print("顯示: 原圖 | 平均模糊 | 高斯模糊 | 中值模糊")
    print("按任意鍵繼續...")
    cv2.waitKey(0)

    print("\n8. 邊緣檢測")
    print("-"*30)
    edges_canny = cv2.Canny(img, 100, 200)
    edges_sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    edges_sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    edges_sobel = np.sqrt(edges_sobel_x**2 + edges_sobel_y**2)
    edges_sobel = np.uint8(np.clip(edges_sobel, 0, 255))

    edges_laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    edges_laplacian = np.uint8(np.absolute(edges_laplacian))

    edge_compare = np.hstack([cv2.resize(gray, (250, 170)),
                              cv2.resize(edges_canny, (250, 170)),
                              cv2.resize(edges_sobel, (250, 170)),
                              cv2.resize(edges_laplacian, (250, 170))])
    cv2.imshow('Edge Detection (Gray, Canny, Sobel, Laplacian)', edge_compare)
    print("顯示: 灰階 | Canny | Sobel | Laplacian")
    print("按任意鍵繼續...")
    cv2.waitKey(0)

    print("\n9. 色彩空間轉換")
    print("-"*30)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    color_compare = np.hstack([cv2.resize(img, (200, 150)),
                               cv2.resize(rgb, (200, 150)),
                               cv2.resize(hsv, (200, 150)),
                               cv2.resize(lab, (200, 150))])
    cv2.imshow('Color Spaces (BGR, RGB, HSV, LAB)', color_compare)
    print("顯示: BGR | RGB | HSV | LAB")
    print("按任意鍵繼續...")
    cv2.waitKey(0)

    print("\n10. 圖片上加文字和形狀")
    print("-"*30)
    img_copy = img.copy()

    cv2.rectangle(img_copy, (50, 50), (200, 150), (0, 255, 0), 3)
    cv2.circle(img_copy, (300, 100), 50, (255, 0, 0), -1)
    cv2.line(img_copy, (0, 200), (img_copy.shape[1], 200), (0, 0, 255), 2)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img_copy, 'OpenCV Example', (50, 250), font, 1, (255, 255, 255), 2)
    cv2.putText(img_copy, 'DAY1 Tutorial', (50, 300), font, 0.8, (0, 255, 255), 2)

    cv2.imshow('Drawing on Image', img_copy)
    print("在圖片上繪製:")
    print("- 綠色矩形")
    print("- 藍色圓形")
    print("- 紅色線條")
    print("- 白色和黃色文字")
    print("按任意鍵繼續...")
    cv2.waitKey(0)

    print("\n11. 儲存處理後的圖片")
    print("-"*30)
    output_path = os.path.join(current_dir, 'processed_image.jpg')
    cv2.imwrite(output_path, img_copy)
    print(f"已儲存處理後的圖片到: {output_path}")

    gray_output = os.path.join(current_dir, 'grayscale_image.jpg')
    cv2.imwrite(gray_output, gray)
    print(f"已儲存灰階圖片到: {gray_output}")

    cv2.destroyAllWindows()

    print("\n" + "="*50)
    print("OpenCV 範例結束！")
    print("="*50)