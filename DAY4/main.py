import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 讀取圖片
img_path = os.path.join(os.path.dirname(__file__), 'Image_20250924142436723.bmp')
print(f"圖片路徑: {img_path}")
print(f"檔案是否存在: {os.path.exists(img_path)}")

# 嘗試以不同方式讀取圖片
img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

if img is None:
    # 如果 OpenCV 無法讀取，嘗試以原始資料讀取
    with open(img_path, 'rb') as f:
        # 跳過 BMP header (54 bytes)
        f.seek(54)
        # 讀取原始資料
        raw_data = np.frombuffer(f.read(), dtype=np.uint8)
        # 重塑為圖片 (假設是 8-bit Bayer 格式)
        img = raw_data.reshape(1944, 2592)
        print("以 Bayer 格式讀取圖片")
        # 轉換 Bayer 格式到 RGB
        # 嘗試不同的 Bayer 模式 (GRBG 是常見的)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BayerGR2RGB)
        img = img_rgb
else:
    print(f"圖片形狀: {img.shape}")
    print(f"圖片資料類型: {img.dtype}")

    # 判斷圖片格式
    if len(img.shape) == 2:
        # 如果是單通道，可能是 Bayer 格式
        print("偵測到單通道圖片，可能是 Bayer 格式")
        # 嘗試不同的 Bayer 轉換模式
        try:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BayerGR2RGB)
            print("使用 BayerGR2RGB 轉換")
        except:
            try:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BayerRG2RGB)
                print("使用 BayerRG2RGB 轉換")
            except:
                try:
                    img_rgb = cv2.cvtColor(img, cv2.COLOR_BayerBG2RGB)
                    print("使用 BayerBG2RGB 轉換")
                except:
                    img_rgb = cv2.cvtColor(img, cv2.COLOR_BayerGB2RGB)
                    print("使用 BayerGB2RGB 轉換")
        img = img_rgb
    elif len(img.shape) == 3:
        # 如果是三通道 BGR 圖片
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        print(f"未知的圖片格式: shape = {img.shape}")
        img_rgb = img

# 1. 轉灰階
if len(img.shape) == 3:
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
else:
    gray = img

# 2. 模糊化 (使用高斯模糊)
blurred = cv2.GaussianBlur(gray, (13, 13), 0)

# 3. Canny邊緣檢測
edges = cv2.Canny(blurred, 100, 120)

# 4. 霍夫找圓
circles = cv2.HoughCircles(
    blurred,
    cv2.HOUGH_GRADIENT,
    dp=1,
    minDist=20,
    param1=50,
    param2=30,
    minRadius=5,
    maxRadius=50
)

# 在原圖上繪製找到的圓
result = img.copy() if len(img.shape) == 3 else cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
if circles is not None:
    circles = np.uint16(np.around(circles))
    print(f"找到 {len(circles[0])} 個圓")

    # 過濾只保留四個角落的圓
    if len(circles[0]) >= 4:
        # 取得所有圓的座標
        all_circles = circles[0]

        # 計算每個圓到四個角的距離
        h, w = gray.shape
        corners = [(0, 0), (w, 0), (0, h), (w, h)]  # 左上、右上、左下、右下
        corner_circles = []

        for corner in corners:
            # 找到離這個角最近的圓
            min_dist = float('inf')
            closest_circle = None
            for circle in all_circles:
                dist = np.sqrt((circle[0] - corner[0])**2 + (circle[1] - corner[1])**2)
                if dist < min_dist:
                    min_dist = dist
                    closest_circle = circle
            if closest_circle is not None and not any(np.array_equal(closest_circle, c) for c in corner_circles):
                corner_circles.append(closest_circle)

        # 只繪製四個角落的圓
        for i, circle in enumerate(corner_circles):
            # 繪製圓形 (加粗、使用亮黃色)
            cv2.circle(result, (circle[0], circle[1]), circle[2], (255, 255, 0), 5)
            # 繪製圓心 (加大、使用亮紅色)
            cv2.circle(result, (circle[0], circle[1]), 5, (255, 0, 0), -1)
            # 標記角落位置 (加大字體、使用亮藍色)
            corner_names = ['左上', '右上', '左下', '右下']
            cv2.putText(result, corner_names[i], (circle[0]-30, circle[1]-25),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 150, 255), 3)

        print(f"過濾後保留 {len(corner_circles)} 個角落圓")
    else:
        # 如果圓少於4個，全部繪製
        for i in circles[0, :]:
            cv2.circle(result, (i[0], i[1]), i[2], (255, 255, 0), 5)
            cv2.circle(result, (i[0], i[1]), 5, (255, 0, 0), -1)
        print(f"圓少於4個，全部顯示")
else:
    print("沒有找到圓")

# 展示所有步驟的結果
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# 原圖
if len(img.shape) == 3:
    axes[0, 0].imshow(img)
else:
    axes[0, 0].imshow(gray, cmap='gray')
axes[0, 0].set_title('1. 原圖', fontsize=14)
axes[0, 0].axis('off')

# 灰階圖
axes[0, 1].imshow(gray, cmap='gray')
axes[0, 1].set_title('2. 灰階圖', fontsize=14)
axes[0, 1].axis('off')

# 模糊化
axes[0, 2].imshow(blurred, cmap='gray')
axes[0, 2].set_title('3. 高斯模糊', fontsize=14)
axes[0, 2].axis('off')

# Canny邊緣檢測
axes[1, 0].imshow(edges, cmap='gray')
axes[1, 0].set_title('4. Canny邊緣檢測', fontsize=14)
axes[1, 0].axis('off')

# 霍夫找圓結果
axes[1, 1].imshow(result)
axes[1, 1].set_title('5. 霍夫找圓結果', fontsize=14)
axes[1, 1].axis('off')

# 隱藏第六個子圖
axes[1, 2].axis('off')

plt.suptitle('OpenCV 圖像處理步驟展示', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# 也保存結果圖片
cv2.imwrite('result_circles.jpg', cv2.cvtColor(result, cv2.COLOR_RGB2BGR))
print("結果已保存為 result_circles.jpg")