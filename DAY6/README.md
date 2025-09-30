# DAY6：智慧視覺檢測整合

- **作者**：harry123180
- **主題**：將 GUI、YOLO 與量測流程串接成示範工具

## 檔案說明
- `smart_inspection_app.py`：主程式，支援載入圖片、執行 YOLO 推論與簡單毫米換算。
- `application.png` / `application.ico`：可用於打包成桌面應用時的圖示。

## 範例流程
```bash
pip install customtkinter ultralytics opencv-python pillow
python smart_inspection_app.py
```
1. 先載入 Day3 訓練好的權重 (`DAY3/runs/demo_yolo11/weights/best.pt`) 或原始 `yolo11n.pt`。
2. 點選「載入圖片」後再按「執行 YOLO 推論」。
3. 輸入 mm/pixel 換算值即可估算偵測框的寬度。

## 延伸建議
- 將像素換算改為雙點校正，提升量測準確度。
- 加入攝影機即時串流模式，模擬產線檢測。
- 搭配 Day5 的介面改造，加入報表輸出與歷史紀錄。
