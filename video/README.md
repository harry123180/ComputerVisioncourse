# video - 影片素材

此資料夾存放課程使用的影片素材。

## 檔案說明

| 檔案 | 說明 | 用途 |
|------|------|------|
| `dancer.mp4` | 舞者動作影片 | DAY2 Mediapipe 姿勢分析 |
| `example.mp4` | 範例影片 | 一般測試用途 |

## 使用方式

這些影片主要供 DAY2 的 Mediapipe 姿勢分析腳本使用：

```bash
cd DAY2
python pose_video_report.py  # 會讀取 ../video/ 內的影片
```
