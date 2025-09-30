"""Day 2：影片批次姿勢摘要"""
from __future__ import annotations
from pathlib import Path
import csv

# Author: harry123180

try:
    import cv2
    import mediapipe as mp
except ImportError as exc:  # pragma: no cover
    raise SystemExit("請先安裝 opencv-python 與 mediapipe 套件") from exc


def iter_video_frames(video_path: Path):
    """逐格讀取影片，yield (索引, frame)"""
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"無法開啟影片: {video_path}")
    index = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        index += 1
        yield index, frame
    cap.release()


def main() -> None:
    """建立影片的簡易姿勢角度紀錄"""
    video_dir = Path(__file__).resolve().parent.parent / "video"
    videos = sorted(video_dir.glob("*.mp4"))
    if not videos:
        raise FileNotFoundError("請在 video 資料夾準備 mp4 示範影片")

    pose = mp.solutions.pose.Pose()
    csv_path = Path(__file__).resolve().parent / "pose_report.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["video", "frame", "torso_angle_degree"])

        for video_path in videos:
            for index, frame in iter_video_frames(video_path):
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = pose.process(rgb)
                if not result.pose_landmarks:
                    continue

                landmarks = result.pose_landmarks.landmark
                shoulder_center = (
                    (landmarks[11].x + landmarks[12].x) / 2,
                    (landmarks[11].y + landmarks[12].y) / 2,
                )
                hip_center = (
                    (landmarks[23].x + landmarks[24].x) / 2,
                    (landmarks[23].y + landmarks[24].y) / 2,
                )
                dx = hip_center[0] - shoulder_center[0]
                dy = hip_center[1] - shoulder_center[1]
                # 使用 fastAtan2 快速求出軀幹傾斜角度 (度數)
                angle = cv2.fastAtan2(dy, dx)
                writer.writerow([video_path.name, index, round(angle, 2)])

    print(f"統計表已輸出到 {csv_path.name}")


if __name__ == "__main__":
    main()
