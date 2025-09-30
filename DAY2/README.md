# DAY2：Mediapipe 姿勢辨識

- **作者**：harry123180
- **主題**：運用 Mediapipe Pose 做即時與離線的姿勢分析

## 環境準備
```bash
pip install -r requirements.txt
```

## 腳本概覽
- `pose_live_demo.py`：使用攝影機即時繪製骨架。
- `pose_video_report.py`：批次讀取 `video/` 內的 MP4，輸出 `pose_report.csv`。
- `pose_squat_counter.py`：用膝蓋角度粗略統計深蹲次數。

## 使用提醒
- 若無攝影機，可先執行 `pose_video_report.py` 了解離線流程。
- `pose_squat_counter.py` 判斷條件較簡易，適合課堂示範概念。
- 執行時若出現模組缺失訊息，請確認 requirements 是否安裝完成。
