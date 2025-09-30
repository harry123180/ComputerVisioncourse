# DAY1：OpenCV 入門練習

- **作者**：harry123180
- **主題**：熟悉影像讀取、轉換、幾何操作與簡易檢測

## 使用方式
1. 建議在虛擬環境中安裝 `opencv-python`：
   ```bash
   pip install opencv-python
   ```
2. 每個腳本可獨立執行，請在 `DAY1/` 目錄下使用 Python 直接執行：
   ```bash
   python step01_read_image.py
   ```
3. 若需要自訂影像，請將 JPG 檔放在 `DAY1/bright front and back/` 或同層目錄。

## 腳本說明
- `step01_read_image.py`：讀取範例圖並顯示在視窗之中。
- `step02_to_grayscale.py`：保存灰階版本的圖片，適合後續做分析。
- `step03_resize_image.py`：將圖片等比例縮到寬度 640 pixel。
- `step04_draw_shapes.py`：在圖片四周畫框與文字示範。
- `step05_detect_edges.py`：以 Canny 檢測輪廓線條。
- `step06_detect_circles.py`：透過霍夫變換找出圓形並標記。

## 備註
- 每個腳本都自動尋找同資料夾內第一張 JPG 圖片。
- 產生的預覽檔案會與原圖放在一起，檔名包含操作描述。
- 建議在教學時逐步展示，方便學員確認每個處理階段的結果。
