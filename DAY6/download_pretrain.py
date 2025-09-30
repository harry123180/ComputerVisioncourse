import urllib.request
import os

def download_yolov11_model(model_type='n', save_dir='./'):
    """
    下載YOLOv11模型
    model_type: 'n', 's', 'm', 'l', 'x'
    """
    
    # 模型檔案資訊（根據您提供的列表）
    model_info = {
        'n': {'name': 'yolo11n.pt', 'size': '5.35 MB'},
        's': {'name': 'yolo11s.pt', 'size': '18.4 MB'},
        'm': {'name': 'yolo11m.pt', 'size': '38.8 MB'},
        'l': {'name': 'yolo11l.pt', 'size': '49 MB'},
        'x': {'name': 'yolo11x.pt', 'size': '109 MB'}
    }
    
    if model_type not in model_info:
        print(f"錯誤：未知的模型類型 {model_type}")
        return None
    
    filename = model_info[model_type]['name']
    expected_size = model_info[model_type]['size']
    
    # 正確的下載URL（注意是yolo11不是yolov11）
    url = f"https://github.com/ultralytics/assets/releases/download/v8.3.0/{filename}"
    
    save_path = os.path.join(save_dir, filename)
    
    print(f"下載模型: {filename}")
    print(f"預期大小: {expected_size}")
    print(f"下載網址: {url}")
    
    try:
        # 下載檔案
        urllib.request.urlretrieve(url, save_path)
        
        # 檢查檔案
        if os.path.exists(save_path):
            actual_size = os.path.getsize(save_path) / (1024*1024)
            print(f"下載完成！")
            print(f"實際大小: {actual_size:.2f} MB")
            return save_path
            
    except Exception as e:
        print(f"下載失敗: {e}")
        return None

# 使用範例
if __name__ == "__main__":
    # 下載nano版本
    download_yolov11_model('s')
    
    # 下載所有版本
    # for size in ['n', 's', 'm', 'l', 'x']:
    #     download_yolov11_model(size)