"""Day 3：使用訓練後模型進行推論"""
from __future__ import annotations
from pathlib import Path

# Author: harry123180

try:
    from ultralytics import YOLO
except ImportError as exc:  # pragma: no cover
    raise SystemExit("請先安裝 ultralytics 套件：pip install ultralytics") from exc


def main() -> None:
    """對驗證集圖片進行推論並輸出帶標註的結果"""
    day_dir = Path(__file__).resolve().parent
    runs_dir = day_dir / "runs" / "demo_yolo11" / "weights"
    weight_files = list(runs_dir.glob("last.pt")) or list(runs_dir.glob("best.pt"))
    if not weight_files:
        raise FileNotFoundError("請先完成訓練，在 runs/demo_yolo11/weights/ 找不到模型")

    model = YOLO(str(weight_files[0]))

    valid_images = sorted((day_dir / "dataset/extracted" / "valid" / "images").glob("*.*"))
    if not valid_images:
        raise FileNotFoundError("驗證集沒有圖片，請確認資料集完整")

    image_path = valid_images[0]
    print(f"對 {image_path.name} 進行推論")

    # save=True 會自動輸出結果在 runs/predict 目錄
    model.predict(source=str(image_path), save=True, name="demo_predict")
    print("完成推論，請到 runs/demo_predict/ 查看結果圖檔")


if __name__ == "__main__":
    main()
