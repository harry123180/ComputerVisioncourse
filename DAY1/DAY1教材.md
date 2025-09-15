# DAY1: NumPy、OpenCV 與 PIL 基礎教學

## 什麼是 NumPy？
NumPy 是 Python 處理數字和陣列的工具。想像它就像 Excel 表格，但更強大。
- 主要用來處理多維陣列（就是很多數字排在一起）
- 做數學運算超快
- 是處理圖片的基礎（圖片就是一堆數字）

## 什麼是 OpenCV？
OpenCV 是專門處理圖片和影片的工具包。
- 可以讀取、顯示、儲存圖片
- 可以做各種圖片處理（模糊、銳利化、找邊緣等）
- 電腦視覺的瑞士刀

## 什麼是 PIL (Pillow)？
PIL 是另一個處理圖片的工具，比較簡單好用。
- 適合做簡單的圖片處理
- 轉換圖片格式很方便
- 和其他 Python 工具配合很好

---

## 安裝套件
打開終端機或命令提示字元，輸入：
```bash
pip install numpy opencv-python pillow
```

---

## NumPy 基本操作

### 1. 建立陣列
```python
import numpy as np

# 建立一維陣列（就像一排數字）
arr1 = np.array([1, 2, 3, 4, 5])
print("一維陣列:", arr1)

# 建立二維陣列（就像表格）
arr2 = np.array([[1, 2, 3],
                  [4, 5, 6]])
print("二維陣列:\n", arr2)
```

### 2. 常用的陣列建立方式
```python
# 全部都是0的陣列
zeros = np.zeros((3, 3))  # 3x3 的零陣列

# 全部都是1的陣列
ones = np.ones((2, 4))    # 2x4 的一陣列

# 隨機數字陣列
random_arr = np.random.random((3, 3))  # 3x3 的隨機陣列
```

### 3. 陣列運算
```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# 加法
print("相加:", a + b)  # [5, 7, 9]

# 乘法
print("相乘:", a * b)  # [4, 10, 18]

# 平均值
print("平均:", np.mean(a))  # 2.0
```

---

## OpenCV 基本操作

### 1. 讀取和顯示圖片
```python
import cv2

# 讀取圖片
img = cv2.imread('圖片路徑.jpg')

# 顯示圖片
cv2.imshow('視窗名稱', img)
cv2.waitKey(0)  # 等待按鍵
cv2.destroyAllWindows()  # 關閉視窗
```

### 2. 儲存圖片
```python
# 儲存圖片
cv2.imwrite('新圖片.jpg', img)
```

### 3. 轉換顏色
```python
# BGR 轉灰階（黑白）
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# BGR 轉 RGB（OpenCV 預設是 BGR）
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
```

---

## PIL (Pillow) 基本操作

### 1. 開啟和顯示圖片
```python
from PIL import Image

# 開啟圖片
img = Image.open('圖片路徑.jpg')

# 顯示圖片
img.show()

# 取得圖片資訊
print("大小:", img.size)  # (寬, 高)
print("模式:", img.mode)  # RGB, RGBA, L(灰階) 等
```

### 2. 調整圖片大小
```python
# 調整大小
new_size = (300, 200)
resized = img.resize(new_size)

# 縮圖（保持比例）
img.thumbnail((300, 300))
```

### 3. 轉換格式
```python
# 轉成灰階
gray = img.convert('L')

# 儲存成不同格式
img.save('新圖片.png')
```

---

## 三個工具的比較

| 功能 | NumPy | OpenCV | PIL |
|------|-------|--------|-----|
| 主要用途 | 數學運算 | 電腦視覺 | 簡單圖片處理 |
| 速度 | 最快 | 快 | 普通 |
| 學習難度 | 中等 | 較難 | 簡單 |
| 圖片格式 | 陣列 | BGR 陣列 | PIL Image |

---

## 實作練習

### 練習 1: 用 NumPy 建立棋盤圖案
```python
import numpy as np
import cv2

# 建立 8x8 的棋盤
board = np.zeros((8, 8))
board[1::2, ::2] = 1
board[::2, 1::2] = 1

# 放大顯示
board_large = np.kron(board, np.ones((50, 50))) * 255
cv2.imshow('棋盤', board_large.astype(np.uint8))
cv2.waitKey(0)
```

### 練習 2: 讀取圖片並轉換
```python
# 用 OpenCV 讀取
img_cv = cv2.imread('test.jpg')

# 轉成 PIL
img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))

# 轉成 NumPy 陣列
img_np = np.array(img_pil)

print("圖片形狀:", img_np.shape)  # (高, 寬, 通道數)
```

---

## 今日重點整理
1. NumPy 是處理陣列的基礎工具
2. OpenCV 適合做複雜的圖片處理
3. PIL 適合做簡單快速的圖片操作
4. 三個工具可以互相轉換使用

## 作業
1. 用 NumPy 建立一個彩虹漸層圖
2. 用 OpenCV 讀取一張圖片並轉成黑白
3. 用 PIL 將圖片縮小一半並另存新檔