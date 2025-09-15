import numpy as np

print("="*50)
print("NumPy 範例程式")
print("="*50)

print("\n1. 建立基本陣列")
print("-"*30)
arr1 = np.array([1, 2, 3, 4, 5])
print("一維陣列:", arr1)
print("陣列形狀:", arr1.shape)
print("陣列類型:", arr1.dtype)

arr2 = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
print("\n二維陣列:")
print(arr2)
print("陣列形狀:", arr2.shape)

print("\n2. 快速建立陣列")
print("-"*30)
zeros = np.zeros((3, 4))
print("零陣列 (3x4):")
print(zeros)

ones = np.ones((2, 3))
print("\n一陣列 (2x3):")
print(ones)

eye = np.eye(4)
print("\n單位矩陣 (4x4):")
print(eye)

arange = np.arange(0, 10, 2)
print("\n等差數列 (0到10，間隔2):", arange)

linspace = np.linspace(0, 1, 5)
print("線性空間 (0到1，分5個點):", linspace)

print("\n3. 隨機陣列")
print("-"*30)
random_int = np.random.randint(1, 10, size=(3, 3))
print("隨機整數陣列 (1-9):")
print(random_int)

random_float = np.random.random((2, 4))
print("\n隨機浮點數陣列 (0-1):")
print(random_float)

normal = np.random.normal(0, 1, (3, 3))
print("\n常態分布陣列 (平均0，標準差1):")
print(normal)

print("\n4. 陣列運算")
print("-"*30)
a = np.array([1, 2, 3, 4])
b = np.array([5, 6, 7, 8])

print("陣列 a:", a)
print("陣列 b:", b)
print("a + b =", a + b)
print("a - b =", a - b)
print("a * b =", a * b)
print("a / b =", a / b)
print("a ** 2 =", a ** 2)

print("\n5. 陣列索引與切片")
print("-"*30)
arr = np.array([[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]])
print("原始陣列:")
print(arr)
print("第一列:", arr[0])
print("第二列第三個元素:", arr[1, 2])
print("前兩列:", arr[:2])
print("第二到第三欄:", arr[:, 1:3])

print("\n6. 陣列變形")
print("-"*30)
arr = np.arange(12)
print("原始陣列:", arr)

reshaped = arr.reshape(3, 4)
print("變形成 3x4:")
print(reshaped)

flattened = reshaped.flatten()
print("攤平:", flattened)

transposed = reshaped.T
print("轉置:")
print(transposed)

print("\n7. 統計運算")
print("-"*30)
data = np.array([[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]])
print("資料:")
print(data)
print("總和:", np.sum(data))
print("平均:", np.mean(data))
print("標準差:", np.std(data))
print("最大值:", np.max(data))
print("最小值:", np.min(data))
print("每列總和:", np.sum(data, axis=1))
print("每欄總和:", np.sum(data, axis=0))

print("\n8. 陣列條件篩選")
print("-"*30)
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
print("原始陣列:", arr)
print("大於5的元素:", arr[arr > 5])
print("偶數元素:", arr[arr % 2 == 0])

mask = (arr > 3) & (arr < 8)
print("3到8之間的元素:", arr[mask])

print("\n9. 陣列合併與分割")
print("-"*30)
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print("陣列 a:", a)
print("陣列 b:", b)

stacked_v = np.vstack([a, b])
print("垂直合併:")
print(stacked_v)

stacked_h = np.hstack([a, b])
print("水平合併:", stacked_h)

concatenated = np.concatenate([a, b])
print("串接:", concatenated)

print("\n10. 實用範例：建立彩虹漸層")
print("-"*30)
rainbow = np.zeros((100, 300, 3), dtype=np.uint8)

for i in range(300):
    if i < 50:
        rainbow[:, i] = [255, i*5, 0]
    elif i < 100:
        rainbow[:, i] = [255-(i-50)*5, 255, 0]
    elif i < 150:
        rainbow[:, i] = [0, 255, (i-100)*5]
    elif i < 200:
        rainbow[:, i] = [0, 255-(i-150)*5, 255]
    elif i < 250:
        rainbow[:, i] = [(i-200)*5, 0, 255]
    else:
        rainbow[:, i] = [255, 0, 255-(i-250)*5]

print("彩虹陣列形狀:", rainbow.shape)
print("資料類型:", rainbow.dtype)
print("可以用 OpenCV 或 PIL 顯示這個彩虹圖片！")

print("\n" + "="*50)
print("NumPy 範例結束！")
print("="*50)