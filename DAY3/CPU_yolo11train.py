from ultralytics import YOLO
import zipfile
import os
from pathlib import Path

# 1. 解壓數據集
def extract_dataset(zip_path, extract_to='./dataset'):
    """解壓Roboflow數據集"""
    # 使用Path處理路徑問題
    zip_path = Path(zip_path).resolve()
    extract_to = Path(extract_to).resolve()
    
    if not zip_path.exists():
        raise FileNotFoundError(f"找不到ZIP檔案: {zip_path}")
    
    print(f"解壓檔案: {zip_path}")
    with zipfile.ZipFile(str(zip_path), 'r') as zip_ref:
        zip_ref.extractall(str(extract_to))
    print(f"數據集已解壓至: {extract_to}")
    return str(extract_to)

# 2. 訓練配置與執行
def train_yolov11_cpu(data_yaml_path):
    """CPU訓練YOLOv11"""
    
    # 載入預訓練模型
    model = YOLO('yolo11n.pt')
    
    # 訓練參數
    results = model.train(
        data=data_yaml_path,      
        epochs=50,                
        imgsz=640,                
        batch=4,                  # CPU使用小批次
        device='cpu',             
        workers=2,                # CPU減少worker數量
        patience=20,              
        save=True,                
        project='runs/train',     
        name='yolov11_cpu',       
        exist_ok=True,            
        pretrained=True,          
        optimizer='SGD',          
        lr0=0.01,                 
        cache=True                
    )
    
    return results
def train_yolov11_gpu(data_yaml_path):
    model = YOLO('yolo11n.pt')
    
    results = model.train(
        data=data_yaml_path,      
        epochs=100,               # GPU 可增加 epochs
        imgsz=640,                
        batch=16,                 # RTX 4060 8GB 可用 16-32
        device=0,                 # 使用 GPU 0
        workers=4,                # GPU 可增加 workers
        patience=20,              
        save=True,                
        project='runs/train',     
        name='yolov11_gpu',       
        exist_ok=True,            
        pretrained=True,          
        optimizer='AdamW',        # GPU 建議用 AdamW
        lr0=0.001,                
        cache='ram',              # 載入記憶體加速
        amp=True                  # 混合精度訓練
    )
    return results
# 3. 主程序
if __name__ == "__main__":
    # 使用絕對路徑或相對路徑
    current_dir = Path(__file__).parent
    
    # 方式1: 使用絕對路徑
    zip_file = r"D:\AWORKSPACE\Github\ComputerVisioncourse\DAY3\rock-paper-scissors.v14i.yolov11.zip"
    
    # 方式2: 使用相對路徑（如果zip在同目錄）
    # zip_file = current_dir / "rock-paper-scissors.v14i.yolov11.zip"
    
    # 解壓目錄
    dataset_dir = current_dir / "dataset_extracted"
    
    # 解壓檔案
    dataset_path = extract_dataset(zip_file, dataset_dir)
    
    # 尋找data.yaml
    data_yaml = None
    for root, dirs, files in os.walk(dataset_path):
        if 'data.yaml' in files:
            data_yaml = os.path.join(root, 'data.yaml')
            print(f"找到data.yaml: {data_yaml}")
            break
    
    if not data_yaml:
        raise FileNotFoundError("找不到data.yaml檔案")
    
    # 開始訓練
    print("開始CPU訓練...")
    results = train_yolov11_gpu(data_yaml)
    
    # 取得最佳模型路徑
    best_model = Path('runs/train/yolov11_cpu/weights/best.pt')
    
    if best_model.exists():
        print(f"\n訓練完成！最佳模型位於: {best_model}")
        
        # 測試推理
        model = YOLO(str(best_model))
        
        # 測試單張圖片（從驗證集取一張）
        valid_images = Path(dataset_path) / 'valid' / 'images'
        if valid_images.exists():
            test_image = list(valid_images.glob('*.jpg'))[0]
            results = model.predict(
                source=str(test_image),
                device='cpu',
                save=True
            )
            print(f"推理測試完成，結果儲存在: runs/detect/")