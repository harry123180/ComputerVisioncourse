# training_data - 機器學習訓練素材

此資料夾存放用於機器學習模型訓練的 ROI 裁剪圖片。

## 資料夾結構

```
training_data/
├── Front/    # 零件正面（9 張）
└── Back/     # 零件背面（22 張）
```

## 圖片規格

| 項目 | 規格 |
|------|------|
| 尺寸 | 224 x 224 像素 |
| 格式 | JPG |
| 內容 | 金屬零件的 ROI 裁剪圖 |

## 產生方式

這些圖片由 `tools/` 資料夾中的 ROI 擷取工具產生：

```bash
# 使用進階版 ROI 擷取工具
python tools/tool06_roi_capture_advanced.py
```

工具會自動：
1. 偵測畫面中的輪廓
2. 以輪廓中心裁剪 224x224 區域
3. 依 Front/Back 模式儲存到對應資料夾

## 用途

這些圖片可用於訓練分類模型，例如：
- 區分零件的正面與背面
- 檢測零件的方向是否正確
- 搭配 `tools/model_coin_classifier.h5` 模型使用
