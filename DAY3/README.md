# DAY3：YOLO11 微調與推論

- **作者**：harry123180
- **主題**：使用 Ultralytics YOLO11 進行資料集微調與推論

## 檔案結構
- `dataset_extracted/`：Roboflow 匯出的資料；請確保 `data.yaml` 存在。
- `My First Project.v1i.yolov11.zip`：原始壓縮檔，可視需求保留備份。
- `models/`：`download_weights.py` 會在此放入預訓練權重。
- `runs/`：訓練與推論輸出皆會放在這裡。

## 腳本說明
- `download_weights.py`：下載 `yolo11n.pt` 預訓練模型。
- `train_yolo.py`：以 `dataset_extracted/data.yaml` 開始訓練，預設 20 epochs。
- `infer_image.py`：讀取訓練成果，對驗證集第一張圖片做推論。

## 推薦流程
```bash
pip install ultralytics
python download_weights.py
python train_yolo.py
python infer_image.py
```

## 備註
- 若要替換資料集，只需更新 `dataset_extracted/` 內容並保持 `data.yaml` 設定。
- 訓練參數可在 `train_yolo.py` 的 `model.train` 區塊調整，課堂上建議少量 epoch 加快示範。
