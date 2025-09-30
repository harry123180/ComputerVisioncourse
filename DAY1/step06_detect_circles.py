"""Day 1 Step 06: 簡易圓形偵測"""
from pathlib import Path
import cv2
import numpy as np

# Author: harry123180


def get_sample_image() -> Path:
    day_dir = Path(__file__).resolve().parent
    # 優先使用之前輸出的邊緣或原始照片
    candidates = list((day_dir / "bright front and back").glob("*.jpg"))
    if not candidates:
        candidates = list(day_dir.glob("*.jpg"))
    if not candidates:
        raise FileNotFoundError("請準備一張含有圓形物件的照片")
    return candidates[0]


def main() -> None:
    image_path = get_sample_image()
    image = cv2.imread(str(image_path))
    if image is None:
        raise RuntimeError("讀取圖片失敗")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # 使用 HoughCircles 偵測圓形
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=40,
        param1=120,
        param2=35,
        minRadius=10,
        maxRadius=200,
    )

    annotated = image.copy()
    count = 0
    if circles is not None:
        for circle in np.round(circles[0]).astype(int):
            count += 1
            center = (circle[0], circle[1])
            radius = circle[2]
            cv2.circle(annotated, center, radius, (0, 255, 0), 2)
            cv2.circle(annotated, center, 3, (0, 0, 255), -1)
    print(f"偵測到 {count} 個圓形")

    output_path = image_path.with_name("circles_overlay.png")
    cv2.imwrite(str(output_path), annotated)
    print(f"結果已輸出到 {output_path.name}")


if __name__ == "__main__":
    main()
