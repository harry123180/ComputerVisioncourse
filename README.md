# Computer Vision Course

這個倉庫整理了 6 天課程的示範程式碼與素材，由 **harry123180** 維護。每一天都對應一個主題，從 OpenCV 入門、Mediapipe 姿勢辨識，到 YOLO 模型微調與 CustomTkinter 圖形界面整合。

---

## 環境需求

- Python 3.10+
- 建議使用 `python -m venv .venv` 建立虛擬環境
- 依各日 `README.md` 安裝對應套件（OpenCV、Mediapipe、Ultralytics、CustomTkinter 等）

> **完全新手？** 請先閱讀 [Getting Started 新手入門指南](docs/README.md)，有完整的圖文教學帶你從零開始設定環境。

---

## 日程重點

### DAY1：OpenCV 入門
- 影像讀取、灰階、縮放、繪圖、邊緣與圓形偵測
- 腳本：`step01_read_image.py` ~ `step06_detect_circles.py`

### DAY2：Mediapipe 姿勢分析
- 即時骨架繪製、影片批次角度統計、深蹲次數估算
- 腳本：`pose_live_demo.py`、`pose_video_report.py`、`pose_squat_counter.py`

### DAY3：YOLO11 微調
- 下載預訓練權重、訓練自訂資料、驗證集推論
- 腳本：`download_weights.py`、`train_yolo.py`、`infer_image.py`

### DAY4：高解析影像處理
- 解析 Bayer 影像並以霍夫變換偵測圓點
- 腳本：`circle_marker_detector.py`

### DAY5：CustomTkinter 介面
- 影像載入、灰階/模糊/邊緣處理 GUI 示範
- 腳本：`inspection_dashboard.py`

### DAY6：智慧檢測整合
- GUI 介面整合 YOLO 推論與簡易毫米換算
- 腳本：`smart_inspection_app.py`

---

## 資料夾結構

```
ComputerVisioncourse/
│
├── DAY1/                      # OpenCV 入門
│   ├── images/                # 來源影像（硬幣照片）
│   ├── output/                # 處理結果
│   └── step01~06_*.py         # 範例腳本
│
├── DAY2/                      # Mediapipe 姿勢分析
│   └── pose_*.py              # 姿勢分析腳本
│
├── DAY3/                      # YOLO11 微調
│   ├── dataset/               # 訓練資料集
│   ├── models/                # 預訓練權重
│   └── runs/                  # 訓練輸出
│
├── DAY4/                      # 高解析影像處理
│   ├── images/                # 高解析度圖片
│   └── output/                # 偵測結果
│
├── DAY5/                      # CustomTkinter GUI
│   └── inspection_dashboard.py
│
├── DAY6/                      # 智慧檢測整合
│   ├── assets/                # 應用程式圖示
│   └── smart_inspection_app.py
│
├── tools/                     # 工具程式集
│   ├── tool01~06_*.py         # 各種工具腳本
│   ├── model_coin_classifier.h5
│   └── model_labels.txt
│
├── calibration_chessboard/    # 相機校正棋盤圖
├── training_data/             # ML 訓練素材
│   ├── Front/                 # 零件正面
│   └── Back/                  # 零件背面
│
├── video/                     # 影片素材
├── output/                    # 共用輸出結果
├── docs/                      # 文件與教學
│   └── setup_guide/           # 環境設定截圖
│
├── ppts/                      # 課程簡報
├── .gitignore
├── AGENTS.md
└── README.md
```

---

## 推薦學習流程

1. 依序閱讀各日 `README.md`，並執行對應腳本體驗功能
2. 於 DAY3 完成 YOLO 訓練，將權重提供給 DAY6 GUI 使用
3. 依 DAY5、DAY6 的延伸建議，嘗試擴充功能或整合自己的專題需求

---

## 快速開始

```bash
# 建立虛擬環境
python -m venv .venv

# 啟動虛擬環境 (Windows)
.venv\Scripts\activate

# 安裝基本套件
pip install opencv-python numpy

# 進入 DAY1 開始學習
cd DAY1
python step01_read_image.py
```

---

歡迎在課後依據專案需求調整程式碼，並持續迭代屬於自己的智慧視覺應用。
