"""Day 1 Step 02: 轉換為灰階影像"""
from pathlib import Path
import cv2

# Author: harry123180


def get_sample_image() -> Path:
    """取得示範影像路徑"""
    day_dir = Path(__file__).resolve().parent
    images_dir = day_dir / "images"

    candidates = list((images_dir / "frontlit_detail").glob("*.jpg"))
    if not candidates:
        candidates = list((images_dir / "backlit_silhouette").glob("*.jpg"))
    if not candidates:
        raise FileNotFoundError("找不到範例圖片，請準備一張 JPG 檔")
    return candidates[0]


def main() -> None:
    """讀取影像並儲存灰階結果"""
    day_dir = Path(__file__).resolve().parent
    output_dir = day_dir / "output"
    output_dir.mkdir(exist_ok=True)

    image_path = get_sample_image()
    image = cv2.imread(str(image_path))
    if image is None:
        raise RuntimeError("無法載入指定的圖片")

    # 轉成灰階，適合之後做邊緣或濾波處理
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    output_path = output_dir / "step02_grayscale.png"
    cv2.imwrite(str(output_path), gray)
    print(f"灰階影像已輸出到 {output_path}")


if __name__ == "__main__":
    main()
