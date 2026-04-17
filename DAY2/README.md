# DAY2：Mediapipe 姿勢辨識

- **作者**：harry123180
- **主題**：運用 Mediapipe Pose 做即時與離線的姿勢分析

## 學習目標

完成 DAY2 後，學員能夠：

1. 理解 Mediapipe Pose 模型的輸入輸出：RGB frame → 33 個 `PoseLandmark`
2. 使用內建繪圖工具在畫面上顯示人體骨架
3. 透過關鍵點座標計算角度、傾斜、運動次數等量化指標
4. 將連續影片結果輸出為 CSV，進行離線分析
5. 建立「姿勢估測 → 幾何計算 → 業務邏輯」的應用模式

## 先備知識

- DAY1 的 OpenCV 基本操作（`VideoCapture`、`cvtColor`、`imshow`）
- 基本向量與角度概念（`atan2`、餘弦定理）

---

## 資料夾結構

```
DAY2/
├── README.md
├── requirements.txt
├── pose_live_demo.py      # 即時骨架繪製
├── pose_video_report.py   # 影片批次分析（產出 CSV）
└── pose_squat_counter.py  # 深蹲計數器
```

---

## 環境準備

```bash
pip install -r requirements.txt
```

---

## 核心概念：Mediapipe Pose 的 33 個關鍵點

Mediapipe Pose 會輸出 33 個人體關鍵點，每個點有 `x`、`y`（0~1 歸一化座標）、`z`（相對深度）、`visibility`（可見度）。

本課程最常用的幾個索引：

| 索引 | 名稱 | 說明 |
|------|------|------|
| 11   | `LEFT_SHOULDER`  | 左肩 |
| 12   | `RIGHT_SHOULDER` | 右肩 |
| 23   | `LEFT_HIP`       | 左髖 |
| 24   | `RIGHT_HIP`      | 右髖 |
| 25   | `LEFT_KNEE`      | 左膝 |
| 27   | `LEFT_ANKLE`     | 左腳踝 |

> 完整 33 點定義請見 [Mediapipe 官方文件](https://developers.google.com/mediapipe/solutions/vision/pose_landmarker)。

**座標轉換常見公式**：

```python
x_pixel = int(landmark.x * frame_width)
y_pixel = int(landmark.y * frame_height)
```

---

## 腳本說明

### 1. `pose_live_demo.py` — 即時骨架繪製

```bash
python pose_live_demo.py
```

**做什麼**：開啟攝影機、讀每一幀、跑 Mediapipe Pose、把 33 個關鍵點與連線畫上去。

**關鍵程式碼**：
```python
pose = mp.solutions.pose.Pose()
rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
result = pose.process(rgb)
drawing.draw_landmarks(frame, result.pose_landmarks,
                      mp.solutions.pose.POSE_CONNECTIONS)
```

**操作**：按 `ESC` 結束。

---

### 2. `pose_video_report.py` — 影片批次分析

```bash
python pose_video_report.py
```

**做什麼**：掃描 `../video/` 內所有 `.mp4`，逐幀計算**軀幹傾斜角**，輸出 `pose_report.csv`。

**CSV 欄位**：

| 欄位 | 說明 |
|------|------|
| `video` | 影片檔名 |
| `frame` | 影格索引（從 1 開始）|
| `torso_angle_degree` | 肩膀中心→髖部中心的連線與水平線的夾角（度數）|

**軀幹角度如何算**：
```python
shoulder_center = midpoint(landmark[11], landmark[12])  # 雙肩中點
hip_center      = midpoint(landmark[23], landmark[24])  # 雙髖中點
angle = atan2(hip_center.y - shoulder_center.y,
              hip_center.x - shoulder_center.x)
```

- 站直時角度接近 **90°**
- 前彎時角度會下降
- 可拿來分析舞蹈片段、瑜伽姿勢或跌倒偵測

---

### 3. `pose_squat_counter.py` — 深蹲計數器

```bash
python pose_squat_counter.py
```

**做什麼**：即時偵測左腳**髖 → 膝 → 踝**三點角度，當角度 `< 90°` 視為「蹲下」，回到直立後加 1 次。

**為何選 90°？**
- 髖—膝—踝夾角在直立時接近 180°，深蹲至大腿平行地面時大約 90°
- 實務上可依學員身高與攝影角度調整（建議 80°~100° 之間）

**角度計算**（`calculate_angle`）：
```python
# 兩條向量 ba、bc 的夾角
ba = a - b
bc = c - b
angle = arccos(dot(ba, bc) / (|ba| * |bc|))
```

**狀態機**：

```
直立 (angle >= 90) ──> 蹲下 (angle < 90) ──> 回到直立 → count += 1
```

---

## 常見問題

### Q1：`mediapipe` 安裝失敗？
- Python 版本需 ≥ 3.8，建議 3.10；Python 3.12 需用 `mediapipe >= 0.10.14`
- Windows 若出錯，升級 `pip install --upgrade pip setuptools wheel` 後再裝

### Q2：即時偵測延遲很高？
- 把 `Pose(model_complexity=0)` 改為輕量模型（預設 1）
- 降低攝影機解析度：`cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)`
- 加上 `rgb.flags.writeable = False` 讓 Mediapipe 不複製資料

### Q3：深蹲計數不準？
- 鏡頭與身體請保持側面 90°，正面拍攝膝蓋角度不易量化
- 遠離攝影機至少 2 公尺，確保 `LEFT_HIP / KNEE / ANKLE` 三個點都在畫面內
- 若環境光太暗，`visibility` 可能偏低，建議 `if landmark.visibility > 0.5` 再納入計算

### Q4：`pose_report.csv` 出現一大堆空白幀？
- 代表該影格沒有偵測到人，屬於正常現象（已在程式用 `continue` 跳過）
- 若幾乎整段都偵測不到，請確認影片人物是否完整入鏡

---

## 延伸任務

- 把 `pose_video_report.py` 改為輸出**關節角度時序折線圖**（matplotlib）
- 參考 [Mediapipe Hands](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker) 做手勢控制
- 將深蹲計數器包裝進 DAY5 的 CustomTkinter 介面，做成「健身小幫手」
- 加入語音提示（`pyttsx3`）在蹲到位時播報
