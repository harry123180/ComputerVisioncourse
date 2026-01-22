# DAY4：高解析影像處理

- **作者**：harry123180
- **主題**：示範如何處理工業相機輸出的高解析度 BMP 影像，並找出圓點標記

---

## 資料夾結構

```
DAY4/
├── README.md
├── circle_marker_detector.py  # 圓點偵測主程式
├── images/                    # 來源影像
│   └── high_res_sample.bmp    # 高解析度範例圖
└── output/                    # 輸出結果
    └── circle_result.png      # 偵測結果（執行後產生）
```

---

## 環境準備

```bash
pip install opencv-python numpy
```

---

## 使用方式

```bash
python circle_marker_detector.py
```

執行後會在 `output/` 資料夾產生 `circle_result.png`，方便在課堂上比較前後效果。

---

## 重點技巧

### Bayer 解碼
針對工業相機輸出的 Bayer 單色影像進行解碼，確保顏色還原正確：
```python
cv2.cvtColor(image, cv2.COLOR_BayerGR2RGB)
```

### 霍夫圓偵測
高斯模糊搭配霍夫圓偵測，可快速標出圓形定位點：
```python
circles = cv2.HoughCircles(
    blurred, cv2.HOUGH_GRADIENT,
    dp=1.2, minDist=40,
    param1=120, param2=40,
    minRadius=10, maxRadius=80
)
```

---

## 延伸應用

- 如需額外的幾何運算，可在此基礎上延伸為尺寸量測流程
- 結合相機校正（`../calibration_chessboard/`）可提升量測精度
