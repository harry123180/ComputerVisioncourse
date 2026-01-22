"""Day 4：圓點標記偵測示範"""
from __future__ import annotations
from pathlib import Path
import cv2
import numpy as np

# Author: harry123180


def load_raw_image() -> np.ndarray:
    """載入 BMP 原始圖，若為 BGR 會轉為 RGB"""
    day_dir = Path(__file__).resolve().parent
    image_path = day_dir / "images" / "high_res_sample.bmp"
    if not image_path.exists():
        raise FileNotFoundError("找不到示範圖片 images/high_res_sample.bmp")

    image = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
    if image is None:
        raise RuntimeError("OpenCV 無法讀取示範圖片")

    if image.ndim == 2:
        # 有些相機輸出 Bayer 單色，轉為可視的灰階
        return cv2.cvtColor(image, cv2.COLOR_BayerGR2RGB)

    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def detect_circles(image: np.ndarray) -> tuple[np.ndarray, int]:
    """使用霍夫變換偵測圓點，並回傳標示後的影像與數量"""
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)

    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=40,
        param1=120,
        param2=40,
        minRadius=10,
        maxRadius=80,
    )

    annotated = image.copy()
    count = 0
    if circles is not None:
        for circle in np.round(circles[0]).astype(int):
            count += 1
            center = (circle[0], circle[1])
            radius = circle[2]
            cv2.circle(annotated, center, radius, (0, 255, 0), 2)
            cv2.circle(annotated, center, 4, (255, 0, 0), -1)
    return annotated, count


def main() -> None:
    image = load_raw_image()
    annotated, count = detect_circles(image)
    print(f"偵測到 {count} 個圓形")

    output_path = Path(__file__).resolve().parent / "output" / "circle_result.png"
    cv2.imwrite(str(output_path), cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR))
    print(f"結果已輸出到 {output_path.name}")


if __name__ == "__main__":
    main()
