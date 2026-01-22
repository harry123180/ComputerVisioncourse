import cv2
import numpy as np

def main():
    # 建立視窗，以便在不同階段顯示圖片
    cv2.namedWindow("Original")
    cv2.namedWindow("Grayscale")
    cv2.namedWindow("Blurred")
    cv2.namedWindow("Canny Edge")
    cv2.namedWindow("Final Result")

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
        # ksize (5, 5) 表示高斯核的大小，數字越大越模糊
        # 0 是 sigmaX，表示高斯核在 X 方向的標準差
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        cv2.imshow("Blurred", blurred)

        # 3. Canny 邊緣檢測
        # 100 和 200 是閾值，數字越小越能檢測出細微的邊緣
        edges = cv2.Canny(blurred, 100, 200)
        cv2.imshow("Canny Edge", edges)

        # 4. 尋找輪廓
        # cv2.RETR_EXTERNAL 只找最外層的輪廓
        # cv2.CHAIN_APPROX_SIMPLE 壓縮水平、垂直、對角線的輪廓點
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 5. 繪製輪廓
        # 複製原始影像，避免在原始影像上繪製
        result_frame = frame.copy()
        # -1 表示繪製所有找到的輪廓
        # (0, 255, 0) 是輪廓的顏色（綠色）
        # 2 是線條粗細
        cv2.drawContours(result_frame, contours, -1, (0, 255, 0), 2)
        cv2.imshow("Final Result", result_frame)

        # 按下 'q' 鍵退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 釋放資源
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()