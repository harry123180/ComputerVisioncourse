import cv2
import os
import numpy as np

print("="*50)
print("OpenCV 範例 07: 模糊效果")
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

    kernel_size = 15
    blur_avg = cv2.blur(img_resized, (kernel_size, kernel_size))
    blur_gaussian = cv2.GaussianBlur(img_resized, (kernel_size, kernel_size), 0)
    blur_median = cv2.medianBlur(img_resized, kernel_size)
    blur_bilateral = cv2.bilateralFilter(img_resized, 15, 75, 75)

    row1 = np.hstack([img_resized, blur_avg])
    row2 = np.hstack([blur_gaussian, blur_median])
    combined = np.vstack([row1, row2])

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(combined, 'Original', (10, 30), font, 0.7, (0, 255, 0), 2)
    cv2.putText(combined, 'Average', (new_width+10, 30), font, 0.7, (0, 255, 0), 2)
    cv2.putText(combined, 'Gaussian', (10, new_height+30), font, 0.7, (0, 255, 0), 2)
    cv2.putText(combined, 'Median', (new_width+10, new_height+30), font, 0.7, (0, 255, 0), 2)

    cv2.imshow('Blur Effects', combined)
    print(f"\n模糊效果展示 (kernel size = {kernel_size}):")
    print("左上：原始圖片")
    print("右上：平均模糊 - 簡單平均，速度快")
    print("左下：高斯模糊 - 自然模糊效果")
    print("右下：中值模糊 - 去除雜訊效果好")
    print("\n額外：雙邊濾波 - 保留邊緣的模糊")
    print("\n按任意鍵關閉視窗...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    save_path = os.path.join(current_dir, 'blur_result.jpg')
    cv2.imwrite(save_path, blur_gaussian)
    print(f"\n高斯模糊圖片已儲存至: {os.path.basename(save_path)}")
    print("\n完成！")