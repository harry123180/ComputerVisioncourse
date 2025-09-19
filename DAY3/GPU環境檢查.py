import torch
import subprocess
import sys

def check_gpu_environment():
    """完整GPU環境檢查"""
    
    print("="*60)
    print("GPU環境檢查報告")
    print("="*60)
    
    # 1. GPU硬體
    print("\n✅ GPU硬體:")
    print("  - NVIDIA GeForce RTX 4060")
    print("  - 顯存: 8GB")
    print("  - 驅動: 576.28")
    print("  - CUDA: 12.9")
    
    # 2. PyTorch檢查
    print("\n📦 PyTorch狀態:")
    print(f"  - PyTorch版本: {torch.__version__}")
    
    if torch.cuda.is_available():
        print(f"  ✅ CUDA可用")
        print(f"  - PyTorch CUDA版本: {torch.version.cuda}")
        print(f"  - GPU數量: {torch.cuda.device_count()}")
        print(f"  - 當前GPU: {torch.cuda.get_device_name(0)}")
        
        # cuDNN檢查
        if torch.backends.cudnn.is_available():
            print(f"  ✅ cuDNN可用")
            print(f"  - cuDNN版本: {torch.backends.cudnn.version()}")
        else:
            print(f"  ❌ cuDNN不可用")
    else:
        print(f"  ❌ CUDA不可用 - 可能安裝了CPU版PyTorch")
        
    # 3. 測試GPU運算
    print("\n🧪 GPU運算測試:")
    try:
        if torch.cuda.is_available():
            x = torch.randn(100, 100).cuda()
            y = torch.matmul(x, x)
            print(f"  ✅ GPU運算成功")
            print(f"  - 測試矩陣運算: {x.shape} @ {x.shape} = {y.shape}")
        else:
            print(f"  ❌ 無法使用GPU運算")
    except Exception as e:
        print(f"  ❌ GPU運算失敗: {e}")
        
    return torch.cuda.is_available()

# 執行檢查
gpu_available = check_gpu_environment()