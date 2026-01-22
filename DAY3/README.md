# DAY3：YOLO11 微調與推論

- **作者**：harry123180
- **主題**：使用 Ultralytics YOLO11 進行資料集微調與推論

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
├── models/                # 預訓練權重（執行 download_weights.py 後產生）
└── runs/                  # 訓練與推論輸出
```

---

## 環境準備

```bash
pip install ultralytics
```

---

## 推薦流程

### Step 1：下載預訓練權重

```bash
python download_weights.py
```

執行後會在 `models/` 資料夾產生 `yolo11n.pt`。

### Step 2：訓練模型

```bash
python train_yolo.py
```

使用 `dataset/extracted/data.yaml` 開始訓練，預設 20 epochs。
訓練成果會輸出到 `runs/demo_yolo11/`。

### Step 3：執行推論

```bash
python infer_image.py
```

讀取訓練成果，對驗證集第一張圖片做推論。
結果會輸出到 `runs/demo_predict/`。

---

## 備註

- 若要替換資料集，只需更新 `dataset/extracted/` 內容並保持 `data.yaml` 設定
- 訓練參數可在 `train_yolo.py` 的 `model.train` 區塊調整
- 課堂上建議少量 epoch 加快示範
- 訓練好的權重可供 DAY6 的 GUI 應用載入使用
