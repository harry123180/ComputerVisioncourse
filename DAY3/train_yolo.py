"""Day 3：訓練 YOLO11 模型"""
from __future__ import annotations
from pathlib import Path

# Author: harry123180

try:
    from ultralytics import YOLO
except ImportError as exc:  # pragma: no cover
    raise SystemExit("請先安裝 ultralytics 套件：pip install ultralytics") from exc


def main() -> None:
    """以 Roboflow 匯出的資料集進行快速微調"""
    day_dir = Path(__file__).resolve().parent
    data_yaml = day_dir / "dataset_extracted" / "data.yaml"
    if not data_yaml.exists():
        raise FileNotFoundError("找不到 data.yaml，請先解壓縮資料集")

    weights = day_dir / "models" / "yolo11n.pt"
    if not weights.exists():
        raise FileNotFoundError("缺少預訓練權重，請先執行 download_weights.py")

    model = YOLO(str(weights))

    # 以較少 epochs 做示範，避免課堂耗時過久
    model.train(
        data=str(data_yaml),
        epochs=20,
        imgsz=640,
        project=str(day_dir / "runs"),
        name="demo_yolo11",
    )

    print("訓練完成，可在 runs/demo_yolo11/ 中找到成果")


if __name__ == "__main__":
    main()
