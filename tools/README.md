# Tools - 工具程式集

此資料夾包含課程中使用的各種工具程式，按學習順序編號。

## 工具列表

| 檔案名稱 | 說明 |
|----------|------|
| `tool01_camera_basic.py` | 最基礎的攝影機開啟範例 |
| `tool02_contour_basic.py` | 基礎輪廓偵測（多視窗展示處理流程） |
| `tool03_contour_area.py` | 輪廓偵測 + 面積計算過濾 |
| `tool04_coin_pipeline.py` | 硬幣偵測完整流程（6 階段視覺化） |
| `tool05_roi_capture_simple.py` | ROI 擷取工具（簡易版 GUI） |
| `tool06_roi_capture_advanced.py` | ROI 擷取工具（進階版 GUI，支援 Front/Back 模式） |

## 模型檔案

| 檔案名稱 | 說明 |
|----------|------|
| `model_coin_classifier.h5` | Keras 硬幣分類模型 |
| `model_labels.txt` | 模型分類標籤（Class 1~4） |

## 安裝依賴

```bash
pip install -r requirements.txt
```

## 使用範例

```bash
# 開啟攝影機測試
python tool01_camera_basic.py

# 硬幣偵測流程展示
python tool04_coin_pipeline.py

# ROI 擷取工具（進階版）
python tool06_roi_capture_advanced.py
```

## 工具說明

### tool01 ~ tool03：基礎學習
適合初學者了解 OpenCV 的基本操作：攝影機讀取、灰階轉換、模糊化、邊緣偵測、輪廓尋找。

### tool04：硬幣偵測流程
展示完整的影像處理 pipeline，包含 6 個階段的視覺化：
1. Original（原始影像）
2. Gray（灰階）
3. Blur（高斯模糊）
4. Edges（Canny 邊緣）
5. Contours（輪廓）
6. Detected Circles（偵測結果）

### tool05 ~ tool06：ROI 擷取工具
用於擷取 224x224 的 ROI 影像，供機器學習模型訓練使用。
- **tool05**：簡易版，自動偵測單一輪廓並裁剪
- **tool06**：進階版，支援 Front/Back 模式切換、Canny 閾值調整
