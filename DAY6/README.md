# DAY6：智慧視覺檢測整合

- **作者**：harry123180
- **主題**：將 GUI、YOLO 與量測流程串接成示範工具

---

## 資料夾結構

```
DAY6/
├── README.md
├── smart_inspection_app.py  # 主程式
├── smart_vision_tool.spec   # PyInstaller 打包設定
└── assets/                  # 應用程式資源
    ├── application.png      # 應用圖示（PNG）
    └── application.ico      # 應用圖示（ICO）
```

---

## 環境準備

```bash
pip install customtkinter ultralytics opencv-python pillow
```

---

## 執行方式

```bash
python smart_inspection_app.py
```

---

## 使用流程

### Step 1：載入模型權重
點選「載入權重」，可選擇：
- DAY3 訓練好的權重：`../DAY3/runs/demo_yolo11/weights/best.pt`
- 或原始預訓練模型：`yolo11n.pt`

### Step 2：載入圖片
點選「載入圖片」選擇要檢測的圖片。

### Step 3：執行推論
點選「執行 YOLO 推論」，系統會自動標註偵測到的物件。

### Step 4：尺寸換算（選用）
輸入 mm/pixel 換算值，即可估算偵測框的實際寬度。

---

## 功能說明

| 功能 | 說明 |
|------|------|
| 載入權重 | 載入 YOLO 模型權重檔 |
| 載入圖片 | 從檔案系統選擇圖片 |
| YOLO 推論 | 執行物件偵測並標註結果 |
| 尺寸換算 | 將像素轉換為毫米單位 |

---

## 延伸建議

- 將像素換算改為雙點校正，提升量測準確度
- 加入攝影機即時串流模式，模擬產線檢測
- 搭配 DAY5 的介面改造，加入報表輸出與歷史紀錄
- 使用 `assets/` 中的圖示，打包成獨立桌面應用程式

---

## 打包獨立執行檔（選用）

附上 `smart_vision_tool.spec`，可用 [PyInstaller](https://pyinstaller.org/) 打包成單一 `.exe`：

```bash
pip install pyinstaller
pyinstaller smart_vision_tool.spec
```

打包完成後會在 `dist/smart_vision_tool/` 取得可執行檔，圖示自動套用 `assets/application.ico`。

