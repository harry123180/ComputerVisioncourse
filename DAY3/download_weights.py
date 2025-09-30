"""Day 3：下載 YOLO 權重"""
from __future__ import annotations
from pathlib import Path

# Author: harry123180

try:
    from ultralytics import YOLO
except ImportError as exc:  # pragma: no cover
    raise SystemExit("請先安裝 ultralytics 套件：pip install ultralytics") from exc


def main() -> None:
    """下載 yolo11n 預訓練權重供課堂使用"""
    target = Path(__file__).resolve().parent / "models"
    target.mkdir(exist_ok=True)

    weight_path = target / "yolo11n.pt"
    if weight_path.exists():
        print("預訓練權重已存在，略過下載")
        return

    # 透過 YOLO 類別讀取模型時會自動下載缺少的權重
    print("正在下載 yolo11n.pt，首次執行需稍候片刻...")
    YOLO("yolo11n.pt")
    cache_dir = Path.home() / ".ultralytics" / "models"
    candidates = list(cache_dir.glob("yolo11n.pt"))
    if not candidates:
        raise RuntimeError("找不到下載後的模型，請確認 ultralytics 是否完成下載")

    weight_path.write_bytes(candidates[0].read_bytes())
    print(f"權重已複製到 {weight_path}")


if __name__ == "__main__":
    main()
