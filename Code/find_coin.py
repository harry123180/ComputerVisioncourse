import cv2
import numpy as np
import math

def stack_images(imgs, cols=3, scale=0.9):
    """把多張影像等尺寸拼成網格方便觀察"""
    # 將灰階轉 BGR 以利拼接
    def to_bgr(im):
        return cv2.cvtColor(im, cv2.COLOR_GRAY2BGR) if len(im.shape) == 2 else im

    imgs = [to_bgr(im) for im in imgs if im is not None]
    if not imgs:
        return None
    h, w = imgs[0].shape[:2]
    # 將不同大小影像都統一到第一張大小
    imgs = [cv2.resize(im, (w, h)) for im in imgs]
    rows = math.ceil(len(imgs) / cols)
    grid = []
    for r in range(rows):
        row_imgs = imgs[r*cols:(r+1)*cols]
        if len(row_imgs) < cols:
            row_imgs += [np.zeros_like(imgs[0])] * (cols - len(row_imgs))
        grid.append(cv2.hconcat(row_imgs))
    out = cv2.vconcat(grid)
    if scale != 1.0:
        out = cv2.resize(out, None, fx=scale, fy=scale)
    return out

def main():
    # Windows 常見：用 CAP_DSHOW 可避免開啟延遲；你有多顆鏡頭就把 0 改 1、2...
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # 想固定解析度可解除註解
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("無法開啟攝影機")
        return

    # 可依你的硬幣大小與畫面調整以下參數
    blur_ksize = 11        # 高斯模糊核大小(奇數)
    canny_lo, canny_hi = 50, 120
    min_area, max_area = 500, 200000   # 硬幣面積範圍(像素)，依解析度調整
    min_circularity = 0.78             # 圓度過濾：4πA/P^2 接近 1 越圓
    hough = False                      # 如想用 Hough 圓偵測，設 True 試試

    while True:
        ok, frame = cap.read()
        if not ok:
            print("無法讀取影像")
            break

        original = frame.copy()

        # 1) 讀圖：已在上面 cap.read()
        # 2) 轉灰階
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 3) 模糊化（減少雜訊）
        blur = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)

        # 4) 找邊緣（Canny）
        edges = cv2.Canny(blur, canny_lo, canny_hi)

        # 5) 找輪廓
        contours_info = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours_info[0] if len(contours_info) == 2 else contours_info[1]

        # 視覺化「所有輪廓」的遮罩
        contours_mask = np.zeros_like(gray)
        cv2.drawContours(contours_mask, contours, -1, 255, 1)

        # 6) 找圓形（兩種法：A. 圓度過濾 + 最小外接圓；B. HoughCircles）
        coins_overlay = original.copy()

        if hough:
            # B) Hough 圓偵測（若光照穩定、硬幣邊緣清楚可用）
            # 參數需依畫面調整：param1=Canny高閾值；param2=累積投票閾值；minRadius/maxRadius依硬幣大小
            circles = cv2.HoughCircles(
                blur, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
                param1=120, param2=40, minRadius=10, maxRadius=0
            )
            if circles is not None:
                circles = np.uint16(np.around(circles[0, :]))
                for (x, y, r) in circles:
                    cv2.circle(coins_overlay, (x, y), r, (0, 255, 0), 2)
                    cv2.circle(coins_overlay, (x, y), 2, (0, 0, 255), 3)
        else:
            # A) 用輪廓 + 圓度過濾
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area < min_area or area > max_area:
                    continue
                peri = cv2.arcLength(cnt, True)
                if peri == 0:
                    continue
                circularity = 4 * math.pi * area / (peri * peri)
                if circularity < min_circularity:
                    continue
                # 以最小外接圓作為硬幣的近似
                (x, y), r = cv2.minEnclosingCircle(cnt)
                center, r = (int(x), int(y)), int(r)
                cv2.circle(coins_overlay, center, r, (0, 255, 0), 2)
                cv2.circle(coins_overlay, center, 2, (0, 0, 255), 2)

        # 7) 繪製圓形的輪廓：已在上方 coins_overlay 完成

        # 8) 展示各個階段的圖像（拼圖）
        # 為了排版整齊，把每張縮成相同大小
        h, w = original.shape[:2]
        show_w, show_h = 640, int(640 * h / w)  # 依視窗寬比例縮放
        original_s   = cv2.resize(original, (show_w, show_h))
        gray_s       = cv2.resize(gray, (show_w, show_h))
        blur_s       = cv2.resize(blur, (show_w, show_h))
        edges_s      = cv2.resize(edges, (show_w, show_h))
        contours_s   = cv2.resize(contours_mask, (show_w, show_h))
        overlay_s    = cv2.resize(coins_overlay, (show_w, show_h))

        # 在每張圖左上角打上標籤方便辨識
        def label(img, text):
            im = img.copy()
            cv2.rectangle(im, (0, 0), (180, 28), (0, 0, 0), -1)
            cv2.putText(im, text, (8, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
            return im

        panels = [
            label(original_s, "Original"),
            label(gray_s, "Gray"),
            label(blur_s, "Blur (Gaussian)"),
            label(edges_s, "Edges (Canny)"),
            label(contours_s, "Contours"),
            label(overlay_s, "Detected Circles")
        ]

        grid = stack_images(panels, cols=3, scale=0.95)
        cv2.imshow("Coin Detection Pipeline (press 'q' to quit)", grid)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()