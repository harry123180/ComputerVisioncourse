"""Day 2：即時 Pose 偵測 Demo"""
from __future__ import annotations

# Author: harry123180

try:
    import cv2
    import mediapipe as mp
except ImportError as exc:  # pragma: no cover
    raise SystemExit("請先安裝 opencv-python 與 mediapipe 套件") from exc


def main() -> None:
    """使用攝影機偵測人體骨架"""
    # 建立 Mediapipe Pose 模型
    pose = mp.solutions.pose.Pose()
    drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("找不到攝影機，請確認是否已連接")

    print("按下 ESC 結束 Demo")
    while True:
        ok, frame = cap.read()
        if not ok:
            print("讀取畫面失敗，結束程式")
            break

        # Mediapipe 需要 RGB 影像
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(rgb)

        # 將骨架畫在原始畫面上
        if result.pose_landmarks:
            drawing.draw_landmarks(
                frame,
                result.pose_landmarks,
                mp.solutions.pose.POSE_CONNECTIONS,
            )

        cv2.imshow("Pose Live", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # 27 = ESC
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
