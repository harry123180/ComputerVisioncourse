"""Day 1 Step 02: 轉換為灰階影像"""
from pathlib import Path
import cv2

# Author: harry123180


def get_sample_image() -> Path:
    """取得示範影像路徑"""
    day_dir = Path(__file__).resolve().parent
    candidates = list((day_dir / "bright front and back").glob("*.jpg"))
    if not candidates:
        candidates = list(day_dir.glob("*.jpg"))
    if not candidates:
        raise FileNotFoundError("找不到範例圖片，請準備一張 JPG 檔")
    return candidates[0]


def main() -> None:
    """讀取影像並儲存灰階結果"""
    image_path = get_sample_image()
    image = cv2.imread(str(image_path))
    if image is None:
        raise RuntimeError("無法載入指定的圖片")

    # 轉成灰階，適合之後做邊緣或濾波處理
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    output_path = image_path.with_name("gray_preview.png")
    cv2.imwrite(str(output_path), gray)
    print(f"灰階影像已輸出到 {output_path.name}")


if __name__ == "__main__":
    main()
