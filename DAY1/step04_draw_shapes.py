"""Day 1 Step 04: 在影像上繪製圖形"""
from pathlib import Path
import cv2

# Author: harry123180


def get_sample_image() -> Path:
    day_dir = Path(__file__).resolve().parent
    candidates = list((day_dir / "bright front and back").glob("*.jpg"))
    if not candidates:
        candidates = list(day_dir.glob("*.jpg"))
    if not candidates:
        raise FileNotFoundError("找不到範例圖片，請放一張 JPG")
    return candidates[0]


def main() -> None:
    image_path = get_sample_image()
    image = cv2.imread(str(image_path))
    if image is None:
        raise RuntimeError("無法讀取圖片")

    # 繪製矩形框出主要物件
    height, width = image.shape[:2]
    top_left = (int(width * 0.1), int(height * 0.1))
    bottom_right = (int(width * 0.9), int(height * 0.9))
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 3)

    # 標上文字方便教學說明
    cv2.putText(image, "Demo Box", (top_left[0], top_left[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv2.LINE_AA)

    output_path = image_path.with_name("drawn_overlay.png")
    cv2.imwrite(str(output_path), image)
    print(f"已繪製圖形並輸出到 {output_path.name}")


if __name__ == "__main__":
    main()
