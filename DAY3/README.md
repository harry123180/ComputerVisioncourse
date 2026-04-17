# DAY3：YOLO11 微調與推論

- **作者**：harry123180
- **主題**：使用 Ultralytics YOLO11 進行資料集微調與推論

## 學習目標

完成 DAY3 後，學員能夠：

1. 理解 YOLO 目標偵測的概念：邊界框（bounding box）+ 類別 + 信心度
2. 讀懂 Ultralytics 的資料集格式（`data.yaml` + YOLO 標註）
3. 執行預訓練權重下載、微調、驗證與推論的完整流程
4. 解讀訓練輸出的關鍵 metrics（mAP、precision、recall）
5. 把訓練好的權重交給 DAY6 GUI 進行產線應用

## 先備知識

- DAY1 的 OpenCV 基本操作
- Python 環境管理（虛擬環境、`pip`）
- 若有 GPU，建議先安裝對應 CUDA 版本的 PyTorch

---

## 資料夾結構

```
DAY3/
├── README.md
├── download_weights.py    # 下載預訓練權重
├── train_yolo.py          # 訓練模型
├── infer_image.py         # 執行推論
├── dataset/               # 資料集
│   ├── yolo_coin_dataset.zip  # 原始壓縮檔（備份用）
│   └── extracted/         # 解壓後的資料
│       ├── data.yaml
│       ├── train/
│       ├── valid/
│       └── test/
├── models/                # 預訓練權重（執行 download_weights.py 後產生 yolo11n.pt）
└── runs/                  # 訓練與推論輸出（執行 train_yolo.py / infer_image.py 後產生）
```

> `models/` 目前放置 `.gitkeep` 佔位，初次 clone 時為空資料夾屬正常。

---

## 核心概念

### YOLO 是什麼？

YOLO（You Only Look Once）是一家族的即時目標偵測模型，對整張圖做一次 forward 就同時預測**邊界框**與**類別**。YOLO11 是 Ultralytics 2024 年推出的版本，共有 n / s / m / l / x 五種尺寸，本課程使用最小的 `yolo11n`（nano）以便在 CPU 上也能訓練。

### 資料集格式

Ultralytics 使用 `data.yaml` 描述資料集：

```yaml
train: train/images      # 訓練圖片路徑
val:   valid/images      # 驗證圖片路徑
test:  test/images
nc: 4                    # 類別數 (number of classes)
names: ['1', '5', '10', '50']  # 類別名稱（硬幣面額）
```

每張圖對應一個同名 `.txt`，每一行是一個框：

```
<class_id> <cx> <cy> <w> <h>
```

其中 `cx, cy, w, h` 皆為**歸一化 (0~1)** 的相對座標。

---

## 環境準備

```bash
pip install ultralytics
```

如果要用 GPU 訓練，請依 [PyTorch 官網](https://pytorch.org/get-started/locally/) 指示安裝對應 CUDA 版本的 `torch`。

---

## 推薦流程

### Step 1：下載預訓練權重

```bash
python download_weights.py
```

執行後會在 `models/` 資料夾產生 `yolo11n.pt`（約 5MB）。

### Step 2：訓練模型

```bash
python train_yolo.py
```

**預設設定**：

| 參數 | 值 | 意義 |
|------|------|------|
| `epochs` | 20 | 完整跑過整個訓練集的次數 |
| `imgsz`  | 640 | 訓練時圖片縮放到的大小 |
| `project`| `runs/` | 結果輸出資料夾 |
| `name`   | `demo_yolo11` | 本次訓練名稱 |

訓練成果會輸出到 `runs/demo_yolo11/`，包含：

```
runs/demo_yolo11/
├── weights/
│   ├── best.pt     ← 驗證集最佳模型（推薦使用）
│   └── last.pt     ← 最後一 epoch 模型
├── results.png     ← 訓練曲線
├── confusion_matrix.png
└── val_batch*.jpg  ← 驗證集推論結果範例
```

### Step 3：執行推論

```bash
python infer_image.py
```

預設讀取 `runs/demo_yolo11/weights/best.pt`，對驗證集第一張圖片做推論，結果輸出到 `runs/demo_predict/`。

---

## Metrics 解讀

訓練結束會印出一張表，重點欄位：

| 指標 | 意義 | 合理區間 |
|------|------|----------|
| `P` (Precision) | 預測為正確的有多少真的正確 | > 0.8 |
| `R` (Recall)    | 真實目標有多少被抓到 | > 0.8 |
| `mAP50`  | IoU ≥ 0.5 時的平均精度 | > 0.7 |
| `mAP50-95` | IoU 從 0.5 到 0.95 平均 | > 0.5（難度高）|

> 課堂 20 epochs 僅作示範，真正產線應用至少 100 epochs 起跳。

---

## 常見問題

### Q1：`CUDA out of memory`？
- 在 `train_yolo.py` 的 `model.train(...)` 加入 `batch=8`（或更小）
- 改用 `imgsz=416` 降低圖片大小

### Q2：訓練非常慢？
- 確認是否真的用到 GPU：`import torch; print(torch.cuda.is_available())`
- 沒 GPU 請減少 `epochs`，或改用更小的資料集

### Q3：`find data.yaml error`？
- 一定要先把 `yolo_coin_dataset.zip` 解壓到 `dataset/extracted/`
- `data.yaml` 內的路徑必須相對於 `data.yaml` 本身

### Q4：推論沒任何框？
- 降低信心度門檻：`model.predict(source=..., conf=0.1)`
- 可能訓練還沒收斂，請再跑幾 epochs

---

## 延伸任務

- 換成你自己的資料集（可用 [Roboflow](https://roboflow.com/) 標註後匯出 YOLO 格式）
- 嘗試 `yolo11s`、`yolo11m` 比較速度與精度
- 把 `runs/demo_yolo11/weights/best.pt` 交給 DAY6 GUI 使用
- 寫一個 `infer_video.py` 處理整段影片，輸出帶框的結果
