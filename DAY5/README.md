# DAY5：CustomTkinter GUI 示範

- **作者**：harry123180
- **主題**：將 OpenCV 處理流程包裝成圖形化介面

## 主要腳本
- `inspection_dashboard.py`：簡化版儀表板，可載入圖片並套用灰階、模糊與邊緣偵測。

## 執行方式
```bash
pip install customtkinter opencv-python pillow
python inspection_dashboard.py
```

## 教學提示
- 可以先向學員介紹每個按鈕背後對應的處理函式。
- 狀態欄會顯示當前操作，便於同步說明流程。
- 後續可延伸加入 YOLO 推論或 CSV 報表輸出，作為專題進階任務。
