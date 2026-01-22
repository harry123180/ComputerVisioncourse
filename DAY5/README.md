# DAY5：CustomTkinter GUI 示範

- **作者**：harry123180
- **主題**：將 OpenCV 處理流程包裝成圖形化介面

---

## 資料夾結構

```
DAY5/
├── README.md
├── inspection_dashboard.py  # 主程式
├── PRD.md                   # 產品需求文件（參考用）
└── TODOLIST.md              # 待辦事項（參考用）
```

---

## 環境準備

```bash
pip install customtkinter opencv-python pillow
```

---

## 執行方式

```bash
python inspection_dashboard.py
```

---

## 功能說明

`inspection_dashboard.py` 是一個簡化版的影像處理儀表板，功能包含：

| 功能 | 說明 |
|------|------|
| 載入圖片 | 從檔案系統選擇圖片 |
| 灰階處理 | 將影像轉換為灰階 |
| 模糊處理 | 套用高斯模糊 |
| 邊緣偵測 | 使用 Canny 演算法 |

---

## 教學提示

1. 先向學員介紹每個按鈕背後對應的處理函式
2. 狀態欄會顯示當前操作，便於同步說明流程
3. 可延伸加入 YOLO 推論或 CSV 報表輸出，作為專題進階任務

---

## 延伸建議

- 參考 `PRD.md` 了解完整產品需求規劃
- 參考 `TODOLIST.md` 了解可擴充的功能項目
- 結合 DAY6 的 YOLO 整合範例，打造完整檢測應用
