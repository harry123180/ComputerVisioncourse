# calibration_chessboard - 相機校正圖片

此資料夾存放相機校正用的棋盤格圖片。

## 檔案說明

共 28 張棋盤格圖片，從不同角度拍攝：

```
chessboard_01.bmp ~ chessboard_28.bmp
```

## 用途

這些圖片用於相機內參校正（Camera Calibration），可以：

1. **消除鏡頭畸變**：校正廣角或魚眼鏡頭的桶狀/枕狀畸變
2. **計算內參矩陣**：取得焦距、主點等相機內部參數
3. **提升量測精度**：搭配 DAY4 的高解析影像處理，提升尺寸量測準確度

## 使用範例

```python
import cv2
import numpy as np
from pathlib import Path

# 讀取校正圖片
images = sorted(Path("calibration_chessboard").glob("*.bmp"))

# 設定棋盤格參數（內角點數量）
pattern_size = (9, 6)  # 依實際棋盤格調整

# 執行校正...
```

## 備註

- 圖片格式為 BMP，解析度較高
- 建議使用至少 10-20 張不同角度的圖片進行校正
- 校正結果可儲存為 YAML/JSON 供後續載入使用
