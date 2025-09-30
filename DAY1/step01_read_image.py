"""Day 1 Step 01: 讀取並顯示教學影像"""
from pathlib import Path
import cv2

# Author: harry123180


def get_sample_image() -> Path:
    """尋找範例照片並回傳路徑"""
    day_dir = Path(__file__).resolve().parent
    # 優先使用課程提供的正面照片
    candidates = list((day_dir / "bright front and back").glob("*.jpg"))
    if not candidates:
        # 找不到預設照片時改用資料夾內第一張 JPG
        candidates = list(day_dir.glob("*.jpg"))
    if not candidates:
        raise FileNotFoundError("請在 DAY1 資料夾放入範例 JPG 圖片")
    return candidates[0]


def main() -> None:
    """載入影像並開啟視窗顯示"""
    image_path = get_sample_image()
    print(f"載入檔案: {image_path.name}")

    # 使用 OpenCV 讀取影像
    image = cv2.imread(str(image_path))
    if image is None:
        raise RuntimeError("OpenCV 無法讀取這張圖片，請確認檔案是否完整")

    # 顯示影像並等待任意鍵
    cv2.imshow("Day1 Step01", image)
    print("按任意鍵關閉視窗")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
