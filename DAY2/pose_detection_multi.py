import cv2
import mediapipe as mp
import numpy as np
import os

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def process_video_two_dancers(video_path, output_path=None):
    """
    處理影片進行兩人姿態檢測
    使用分割畫面方式，左右各偵測一人
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"無法開啟影片: {video_path}")
        return

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"影片資訊:")
    print(f"  解析度: {width}x{height}")
    print(f"  FPS: {fps}")
    print(f"  總幀數: {total_frames}")
    print(f"  偵測模式: 分割畫面兩人偵測")

    out = None
    if output_path:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    pose_left = mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        model_complexity=2,
        enable_segmentation=False,
        smooth_landmarks=True)

    pose_right = mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        model_complexity=2,
        enable_segmentation=False,
        smooth_landmarks=True)

    frame_count = 0
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        frame_count += 1
        original_image = image.copy()

        mid_x = width // 2
        left_region = image[:, :mid_x]
        right_region = image[:, mid_x:]

        left_region_rgb = cv2.cvtColor(left_region, cv2.COLOR_BGR2RGB)
        right_region_rgb = cv2.cvtColor(right_region, cv2.COLOR_BGR2RGB)

        results_left = pose_left.process(left_region_rgb)
        results_right = pose_right.process(right_region_rgb)

        image = original_image.copy()

        person_count = 0

        if results_left.pose_landmarks:
            person_count += 1

            temp_image = np.zeros_like(left_region)
            mp_drawing.draw_landmarks(
                temp_image,
                results_left.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=3),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2))

            image[:, :mid_x] = cv2.addWeighted(image[:, :mid_x], 0.7, temp_image, 0.3, 0)

            landmarks = results_left.pose_landmarks.landmark
            if len(landmarks) > 0:
                left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
                right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
                left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
                right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]

                shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
                shoulder_center_y = (left_shoulder.y + right_shoulder.y) / 2
                hip_center_x = (left_hip.x + right_hip.x) / 2
                hip_center_y = (left_hip.y + right_hip.y) / 2

                torso_angle = np.degrees(np.arctan2(
                    hip_center_y - shoulder_center_y,
                    hip_center_x - shoulder_center_x
                ))

                cv2.putText(image, f"Dancer 1 (Left): {torso_angle:.1f} deg",
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        if results_right.pose_landmarks:
            person_count += 1

            temp_image = np.zeros_like(right_region)
            mp_drawing.draw_landmarks(
                temp_image,
                results_right.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2))

            image[:, mid_x:] = cv2.addWeighted(image[:, mid_x:], 0.7, temp_image, 0.3, 0)

            landmarks = results_right.pose_landmarks.landmark
            if len(landmarks) > 0:
                left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
                right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
                left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
                right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]

                shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
                shoulder_center_y = (left_shoulder.y + right_shoulder.y) / 2
                hip_center_x = (left_hip.x + right_hip.x) / 2
                hip_center_y = (left_hip.y + right_hip.y) / 2

                torso_angle = np.degrees(np.arctan2(
                    hip_center_y - shoulder_center_y,
                    hip_center_x - shoulder_center_x
                ))

                cv2.putText(image, f"Dancer 2 (Right): {torso_angle:.1f} deg",
                           (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.line(image, (mid_x, 0), (mid_x, height), (255, 255, 0), 1)

        cv2.putText(image, f"Detected: {person_count} dancers",
                   (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        cv2.putText(image, f"Frame: {frame_count}/{total_frames}",
                   (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow('Two Dancers Pose Detection', image)

        if out:
            out.write(image)

        if cv2.waitKey(5) & 0xFF == 27:
            print("使用者中斷處理")
            break

        if frame_count % 30 == 0:
            print(f"處理進度: {frame_count}/{total_frames} ({frame_count*100/total_frames:.1f}%)")

    pose_left.close()
    pose_right.close()
    cap.release()
    if out:
        out.release()
    cv2.destroyAllWindows()
    print("處理完成！")

def main():
    import sys
    if len(sys.argv) > 1:
        video_folder = sys.argv[1]
    else:
        video_folder = "../video"
        if not os.path.exists(video_folder):
            video_folder = "video"
        if not os.path.exists(video_folder):
            video_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "video")

    if not os.path.exists(video_folder):
        print(f"找不到 video 資料夾: {video_folder}")
        return

    video_files = [f for f in os.listdir(video_folder)
                   if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]

    if not video_files:
        print(f"在 {video_folder} 中找不到影片檔案")
        return

    selected_file = video_files[0]
    print(f"處理影片: {selected_file}")

    input_path = os.path.join(video_folder, selected_file)

    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_filename = f"two_dancers_{selected_file}"
    output_path = os.path.join(output_folder, output_filename)
    print(f"輸出至: {output_path}")

    print("\n開始處理影片 (按 ESC 可中斷)...")
    process_video_two_dancers(input_path, output_path)

if __name__ == "__main__":
    main()