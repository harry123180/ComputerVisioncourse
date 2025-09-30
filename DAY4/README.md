# DAY4：高解析資料前處理

- **作者**：harry123180
- **主題**：示範如何處理工業相機輸出的 BMP 影像，並找出圓點標記

## 檔案說明
- `Image_20250924142436723.bmp`：課程提供的原始樣本。
- `circle_marker_detector.py`：讀取 BMP、轉換色彩並以霍夫變換找圓。

## 使用方式
```bash
pip install opencv-python numpy
python circle_marker_detector.py
```
執行後會輸出 `circle_result.png`，方便在課堂上比較前後效果。

## 重點技巧
- 針對 Bayer 單色影像進行解碼，確保顏色還原正確。
- 高斯模糊搭配霍夫圓偵測，可快速標出圓形定位點。
- 如需額外的幾何運算，可在此基礎上延伸為尺寸量測流程。
