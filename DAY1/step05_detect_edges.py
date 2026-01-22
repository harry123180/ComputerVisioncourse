"""Day 1 Step 05: 邊緣偵測"""
from pathlib import Path
import cv2

# Author: harry123180


def get_sample_image() -> Path:
    day_dir = Path(__file__).resolve().parent
    images_dir = day_dir / "images"

    candidates = list((images_dir / "frontlit_detail").glob("*.jpg"))
    if not candidates:
        candidates = list((images_dir / "backlit_silhouette").glob("*.jpg"))
    if not candidates:
        raise FileNotFoundError("缺少測試圖片")
    return candidates[0]


def main() -> None:
    day_dir = Path(__file__).resolve().parent
    output_dir = day_dir / "output"
    output_dir.mkdir(exist_ok=True)

    image_path = get_sample_image()
    image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise RuntimeError("無法載入圖片")

    # 先做輕微模糊降低雜訊
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    edges = cv2.Canny(blurred, 80, 160)

    output_path = output_dir / "step05_edges.png"
    cv2.imwrite(str(output_path), edges)
    print(f"邊緣檢測結果已存成 {output_path}")


if __name__ == "__main__":
    main()
