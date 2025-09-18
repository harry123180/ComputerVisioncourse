import cv2
import os
import numpy as np

print("="*50)
print("OpenCV 範例 10: 硬幣偵測完整流程")
print("="*50)

# 步驟 1: 讀取圖片
print("\n步驟 1: 讀取圖片")
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
img_path = "D:\\AWORKSPACE\\Github\\ComputerVisioncourse\\DAY1\\backlight\\WIN_20250914_16_47_17_Pro.jpg"
print(f"讀取圖片: {os.path.basename(img_path)}")
img = cv2.imread(img_path)

if img is None:
    print("錯誤：無法讀取圖片！")
else:
    print(f"原始尺寸: {img.shape[1]} x {img.shape[0]}")

    # 步驟 2: Resize 縮放圖片
    print("\n步驟 2: Resize 縮放圖片")
    max_width = 800
    height, width = img.shape[:2]
    scale = max_width / width
    new_width = int(width * scale)
    new_height = int(height * scale)
    img_resized = cv2.resize(img, (new_width, new_height))
    print(f"縮放後尺寸: {new_width} x {new_height}")

    # 保存原始彩色圖片用於最後顯示
    img_display = img_resized.copy()

    # 步驟 3: 轉換成灰階
    print("\n步驟 3: 轉換成灰階")
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    print("已轉換成灰階圖片")

    # 步驟 4: 模糊處理（減少雜訊）
    print("\n步驟 4: 高斯模糊處理")
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    print("已完成模糊處理，kernel size = (9, 9)")

    # 步驟 5: Canny 邊緣檢測
    print("\n步驟 5: Canny 邊緣檢測")
    edges = cv2.Canny(blurred, 30, 100)
    print("已完成邊緣檢測，閾值: 30-100")

    # 步驟 6: 找輪廓
    print("\n步驟 6: 尋找輪廓")
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"找到 {len(contours)} 個輪廓")

    # 步驟 7: 找圓形（使用霍夫圓檢測）
    print("\n步驟 7: 霍夫圓檢測")
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=50,
        param1=100,
        param2=30,
        minRadius=20,
        maxRadius=150
    )

    # 步驟 8: 畫輪廓
    print("\n步驟 8: 繪製輪廓")
    contour_img = img_display.copy()
    cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)
    print(f"繪製了 {len(contours)} 個輪廓")

    # 創建最終結果圖片
    result_img = img_display.copy()

    # 步驟 9: 畫圓形和圓心
    print("\n步驟 9: 繪製圓形和圓心")

    # 如果霍夫圓檢測有結果
    if circles is not None:
        circles = np.uint16(np.around(circles))
        print(f"霍夫圓檢測找到 {circles.shape[1]} 個圓")

        for i in circles[0, :]:
            # 畫圓形輪廓
            cv2.circle(result_img, (i[0], i[1]), i[2], (255, 0, 0), 3)
            # 畫圓心
            cv2.circle(result_img, (i[0], i[1]), 5, (0, 0, 255), -1)
            # 標註半徑
            cv2.putText(result_img, f"R={i[2]}", (i[0]-30, i[1]-i[2]-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
    else:
        print("未檢測到圓形")

    # 步驟 10: 顯示結果
    print("\n步驟 10: 顯示結果")

    # 創建顯示網格
    # 第一行：原圖、灰階、模糊
    row1_1 = cv2.resize(img_resized, (300, 200))
    row1_2 = cv2.resize(cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR), (300, 200))
    row1_3 = cv2.resize(cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR), (300, 200))
    row1 = np.hstack([row1_1, row1_2, row1_3])

    # 第二行：邊緣、輪廓、最終結果
    row2_1 = cv2.resize(cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR), (300, 200))
    row2_2 = cv2.resize(contour_img, (300, 200))
    row2_3 = cv2.resize(result_img, (300, 200))
    row2 = np.hstack([row2_1, row2_2, row2_3])

    # 組合所有圖片
    combined = np.vstack([row1, row2])

    # 加上標題
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(combined, '1.Original', (10, 20), font, 0.5, (255, 255, 255), 1)
    cv2.putText(combined, '2.Grayscale', (310, 20), font, 0.5, (255, 255, 255), 1)
    cv2.putText(combined, '3.Blur', (610, 20), font, 0.5, (255, 255, 255), 1)
    cv2.putText(combined, '4.Edges', (10, 220), font, 0.5, (255, 255, 255), 1)
    cv2.putText(combined, '5.Contours', (310, 220), font, 0.5, (255, 255, 255), 1)
    cv2.putText(combined, '6.Result', (610, 220), font, 0.5, (255, 255, 255), 1)

    cv2.imshow('Coin Detection Pipeline', combined)

    # 顯示大的結果圖
    cv2.imshow('Final Result', result_img)

    print("\n處理流程說明：")
    print("上排：原圖 -> 灰階 -> 模糊")
    print("下排：邊緣 -> 輪廓 -> 最終結果")
    print("\n顏色說明：")
    print("藍色圓：霍夫圓檢測結果")
    print("綠色線：輪廓")
    print("紅色點：圓心位置")
    print("黃色字：半徑數值")
    print("\n按任意鍵關閉視窗...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 儲存結果
    save_path = os.path.join(current_dir, 'coin_detection_result.jpg')
    cv2.imwrite(save_path, result_img)

    pipeline_path = os.path.join(current_dir, 'coin_detection_pipeline.jpg')
    cv2.imwrite(pipeline_path, combined)

    print(f"\n結果已儲存:")
    print(f"  - {os.path.basename(save_path)}")
    print(f"  - {os.path.basename(pipeline_path)}")
    print("\n完成！")