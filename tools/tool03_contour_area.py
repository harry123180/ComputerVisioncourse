import cv2
import numpy as np

def main():
    # 建立視窗，以便在不同階段顯示圖片
    cv2.namedWindow("Original")
    cv2.namedWindow("Grayscale")
    cv2.namedWindow("Blurred")
    cv2.namedWindow("Canny Edge")
    cv2.namedWindow("Final Result with Area")

    # 讀取 Webcam 0
    cap = cv2.VideoCapture(0)

    # 檢查攝影機是否成功開啟
    if not cap.isOpened():
        print("無法開啟 Webcam")
        return

    while True:
        # 讀取影像幀
        ret, frame = cap.read()
        if not ret:
            print("無法讀取影像幀")
            break
        
        # 顯示原始影像
        cv2.imshow("Original", frame)

        # 1. 轉換為灰階
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Grayscale", gray)

        # 2. 高斯模糊化
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        cv2.imshow("Blurred", blurred)

        # 3. Canny 邊緣檢測
        edges = cv2.Canny(blurred, 100, 200)
        cv2.imshow("Canny Edge", edges)

        # 4. 尋找輪廓
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 5. 繪製輪廓並計算面積
        result_frame = frame.copy()

        # 遍歷所有找到的輪廓
        for contour in contours:
            # 忽略太小的雜訊輪廓
            area = cv2.contourArea(contour)
            if area > 500 and area <1500 : # 設定一個閾值，只處理面積大於 500 的輪廓
                # 繪製輪廓
                cv2.drawContours(result_frame, [contour], -1, (0, 255, 0), 2)
                
                # 計算輪廓的中心點
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                else:
                    cX, cY = 0, 0
                
                # 格式化面積文字
                area_text = f"Area: {int(area)}"
                
                # 計算文字的尺寸以定位
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.5
                thickness = 1
                text_size, _ = cv2.getTextSize(area_text, font, font_scale, thickness)
                
                # 將文字寫在輪廓中心靠右下的位置
                # x 座標：中心點 + 10 (向右偏移)
                # y 座標：中心點 + text_size[1] + 10 (向下偏移)
                text_x = cX + 10
                text_y = cY + text_size[1] + 10
                
                cv2.putText(result_frame, area_text, (text_x, text_y), font, font_scale, (0, 0, 255), thickness)

        cv2.imshow("Final Result with Area", result_frame)

        # 按下 'q' 鍵退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 釋放資源
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()