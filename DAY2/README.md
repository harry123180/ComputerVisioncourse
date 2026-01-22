# DAY2：Mediapipe 姿勢辨識

- **作者**：harry123180
- **主題**：運用 Mediapipe Pose 做即時與離線的姿勢分析

---

## 資料夾結構

```
DAY2/
├── README.md
├── requirements.txt
├── pose_live_demo.py      # 即時骨架繪製
├── pose_video_report.py   # 影片批次分析
└── pose_squat_counter.py  # 深蹲計數器
```

---

## 環境準備

```bash
pip install -r requirements.txt
```

---

## 腳本說明

### pose_live_demo.py
使用攝影機即時繪製骨架，展示 Mediapipe Pose 的基本用法。

```bash
python pose_live_demo.py
```

### pose_video_report.py
批次讀取 `../video/` 內的 MP4 檔案，輸出 `pose_report.csv` 統計報告。

```bash
python pose_video_report.py
```

### pose_squat_counter.py
透過膝蓋角度變化粗略統計深蹲次數，適合課堂示範概念。

```bash
python pose_squat_counter.py
```

---

## 使用提醒

- 若無攝影機，可先執行 `pose_video_report.py` 了解離線流程
- `pose_squat_counter.py` 判斷條件較簡易，適合課堂示範概念
- 執行時若出現模組缺失訊息，請確認 requirements 是否安裝完成
- 處理後的影片會輸出到 `../output/` 資料夾
