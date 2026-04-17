# DAY4：高解析影像處理

- **作者**：harry123180
- **主題**：示範如何處理工業相機輸出的高解析度 BMP 影像，並找出圓點標記

## 學習目標

完成 DAY4 後，學員能夠：

1. 理解工業相機常見的 **Bayer** 色彩編碼，並能正確解碼還原影像
2. 處理大尺寸 BMP 影像，避免記憶體與顯示上的問題
3. 使用 `HoughCircles` 進行圓點定位，並調整關鍵參數
4. 將 DAY1 的圓形偵測技巧搬到產線等級的真實影像

## 先備知識

- DAY1 的 OpenCV 基礎（讀檔、灰階、高斯模糊、HoughCircles）
- 對「像素色彩」有基本概念（RGB / BGR）

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

## 核心概念

### 什麼是 Bayer 影像？

工業相機為了降低成本與頻寬，感光元件（CMOS）通常只在每個像素位置放**單一**色彩濾鏡（R、G 或 B），這些單色像素以特定陣列排列，最常見的有：

```
BayerGR：       BayerBG：       BayerRG：       BayerGB：
G R G R ...     B G B G ...     R G R G ...     G B G B ...
R G R G ...     G R G R ...     G B G B ...     B G B G ...
```

原始輸出是**單通道灰度圖**，需要經過「**去馬賽克 (demosaic)**」才能還原成三通道彩色影像。OpenCV 提供對應的轉換常數：

```python
cv2.cvtColor(image, cv2.COLOR_BayerGR2RGB)
cv2.cvtColor(image, cv2.COLOR_BayerBG2BGR)
# ...
```

**如何判斷是哪種 Bayer？**：通常由相機廠商規格決定，若不確定可逐一試過四種，肉眼看哪種色彩正確。

### HoughCircles 參數說明

```python
circles = cv2.HoughCircles(
    blurred,                # 來源影像（單通道 8bit）
    cv2.HOUGH_GRADIENT,     # 演算法（目前僅支援這個）
    dp=1.2,                 # 累加器解析度反比。1 = 同原圖，值越大越模糊
    minDist=40,             # 兩圓心最短距離（避免重複）
    param1=120,             # Canny 高閾值（低閾值自動 = param1/2）
    param2=40,              # 累加器閾值，值越小偵測越多
    minRadius=10,           # 最小半徑
    maxRadius=80            # 最大半徑
)
```

**調參小訣竅**：

| 問題 | 調整方向 |
|------|----------|
| 偵測不到圓 | `param2 ↓`、`minRadius ↓` |
| 誤判太多 | `param2 ↑`、`minDist ↑` |
| 大小圓都要抓 | 拉大 `minRadius / maxRadius` 範圍，或跑兩次 |
| 高解析度很慢 | 先 `cv2.resize` 縮小、處理完再 scale 回去 |

---

## 使用方式

```bash
python circle_marker_detector.py
```

執行後會：

1. 讀取 `images/high_res_sample.bmp`
2. 若是單通道（Bayer）則以 `COLOR_BayerGR2RGB` 解碼；若已是彩色則直接轉 RGB
3. 灰階 → 高斯模糊 → HoughCircles 偵測
4. 在原圖上用綠色圓 + 紅色圓心標示結果
5. 輸出到 `output/circle_result.png`，並在 console 顯示偵測到幾個圓

---

## 常見問題

### Q1：`OpenCV 無法讀取示範圖片`？
- 檢查 `images/high_res_sample.bmp` 是否存在、大小是否正常
- BMP 檔若太大（> 500MB），部分平台需升級 OpenCV

### Q2：顏色看起來怪怪的（偏紫 / 偏綠）？
- Bayer 排列判斷錯誤，請改用 `COLOR_BayerBG2RGB`、`COLOR_BayerRG2RGB`、`COLOR_BayerGB2RGB` 其中一個

### Q3：顯示視窗太大超出螢幕？
- 先 `cv2.resize` 縮小到 1280x720 再 `imshow`，或改用 `cv2.namedWindow("x", cv2.WINDOW_NORMAL)` 讓視窗可縮放

### Q4：輸出圖顏色偏藍？
- 程式最後 `cv2.imwrite` 前做了 `cvtColor(annotated, COLOR_RGB2BGR)`，請確認沒被改掉

---

## 延伸應用

- **幾何量測**：搭配 `calibration_chessboard/` 做鏡頭校正（`cv2.calibrateCamera`），將像素距離換算為實際毫米
- **定位應用**：多圓點可用於印刷電路板對位、自動光學檢測 (AOI)
- **速度優化**：若幀率要求高，先縮圖偵測 → 在原圖 ROI 精修，可大幅降低運算量
- **影像拼接**：高解析度相機搭配移動平台，可以把多張圖拼成超高解析度全景
