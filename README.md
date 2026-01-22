# Computer Vision Course

這個倉庫整理了 6 天課程的示範程式碼與素材，由 **harry123180** 維護。每一天都對應一個主題，從 OpenCV 入門、Mediapipe 姿勢辨識，到 YOLO 模型微調與 CustomTkinter 圖形界面整合。

## 環境需求
- Python 3.10+
- 建議使用 `python -m venv .venv` 建立虛擬環境
- 依各日 `README.md` 安裝對應套件（OpenCV、Mediapipe、Ultralytics、CustomTkinter 等）

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

## 資料夾結構
```
ComputerVisioncourse/
├── DAY1 ~ DAY6/           # 每日主題程式碼與說明文件
├── tools/                  # 工具程式與模型檔
│   ├── tool01_camera_basic.py      # 基礎攝影機開啟
│   ├── tool02_contour_basic.py     # 基礎輪廓偵測
│   ├── tool03_contour_area.py      # 輪廓面積計算
│   ├── tool04_coin_pipeline.py     # 硬幣偵測完整流程
│   ├── tool05_roi_capture_simple.py # ROI 擷取工具（簡易版）
│   ├── tool06_roi_capture_advanced.py # ROI 擷取工具（進階版）
│   ├── model_coin_classifier.h5    # Keras 硬幣分類模型
│   └── model_labels.txt            # 模型標籤檔
├── calibration_chessboard/ # 相機校正用棋盤圖片
├── Front/, Back/          # 硬幣正反面訓練素材
├── img/, video/           # 課程使用的影像與影片素材
├── output/, ppts/         # 產出成果與簡報
└── .gitignore             # Git 忽略設定
```

## 推薦學習流程
1. 依序閱讀各日 `README.md`，並執行對應腳本體驗功能。
2. 於 Day3 完成 YOLO 訓練，將權重提供給 Day6 GUI 使用。
3. 依 Day5、Day6 的 TODO 列表，嘗試擴充功能或整合自己的專題需求。

歡迎在課後依據專案需求調整程式碼，並持續迭代屬於自己的智慧視覺應用。
