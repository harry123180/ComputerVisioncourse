"""Day 1 Step 03: 調整影像尺寸"""
from pathlib import Path
import cv2

# Author: harry123180


def get_sample_image() -> Path:
    day_dir = Path(__file__).resolve().parent
    candidates = list((day_dir / "bright front and back").glob("*.jpg"))
    if not candidates:
        candidates = list(day_dir.glob("*.jpg"))
    if not candidates:
        raise FileNotFoundError("找不到範例圖片，請放入一張 JPG")
    return candidates[0]


def resize_image(image_path: Path, width: int = 640) -> Path:
    """將影像等比例縮放到指定寬度"""
    image = cv2.imread(str(image_path))
    if image is None:
        raise RuntimeError("讀取圖片失敗")

    height, original_width = image.shape[:2]
    scale = width / original_width
    target_size = (width, int(height * scale))

    # 使用 INTER_AREA 可得到較柔和平滑的縮圖
    resized = cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)

    output_path = image_path.with_name("resized_preview.png")
    cv2.imwrite(str(output_path), resized)
    return output_path


def main() -> None:
    image_path = get_sample_image()
    result_path = resize_image(image_path)
    print(f"縮圖已存成 {result_path.name}")


if __name__ == "__main__":
    main()
