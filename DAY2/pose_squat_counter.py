"""Day 2：深蹲次數統計"""
from __future__ import annotations

# Author: harry123180

try:
    import cv2
    import mediapipe as mp
except ImportError as exc:  # pragma: no cover
    raise SystemExit("請先安裝 opencv-python 與 mediapipe 套件") from exc


def calculate_angle(a, b, c) -> float:
    """計算三點角度 (單位: 度)"""
    import math

    ax, ay = a
    bx, by = b
    cx, cy = c
    ab = (ax - bx, ay - by)
    cb = (cx - bx, cy - by)
    dot = ab[0] * cb[0] + ab[1] * cb[1]
    norm_ab = math.hypot(*ab)
    norm_cb = math.hypot(*cb)
    if norm_ab == 0 or norm_cb == 0:
        return 180.0
    cos_angle = max(-1.0, min(1.0, dot / (norm_ab * norm_cb)))
    return math.degrees(math.acos(cos_angle))


def main() -> None:
    """透過膝蓋角度估算深蹲次數"""
    pose = mp.solutions.pose.Pose()
    drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("找不到攝影機，請確認是否已連接")

    squat_count = 0
    is_below_threshold = False

    print("當膝蓋角度低於 90 度會記錄一次深蹲，按 ESC 結束")

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(rgb)

        if result.pose_landmarks:
            drawing.draw_landmarks(
                frame,
                result.pose_landmarks,
                mp.solutions.pose.POSE_CONNECTIONS,
            )

            lmk = result.pose_landmarks.landmark
            left_hip = (lmk[23].x, lmk[23].y)
            left_knee = (lmk[25].x, lmk[25].y)
            left_ankle = (lmk[27].x, lmk[27].y)

            angle = calculate_angle(left_hip, left_knee, left_ankle)
            angle_text = f"Knee: {angle:5.1f}" if angle == angle else "Knee: --"
            cv2.putText(frame, angle_text, (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (50, 220, 220), 2)

            # 小於 90 度代表已經蹲下
            if angle < 90:
                if not is_below_threshold:
                    is_below_threshold = True
            else:
                if is_below_threshold:
                    squat_count += 1
                    is_below_threshold = False

            cv2.putText(frame, f"Squat Count: {squat_count}", (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow("Squat Counter", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"總共完成 {squat_count} 次深蹲")


if __name__ == "__main__":
    main()
