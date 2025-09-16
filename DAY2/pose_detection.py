import cv2
import mediapipe as mp
import numpy as np
import os

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def process_video(video_path, output_path=None):
    """
    處理影片進行姿態檢測

    Args:
        video_path: 輸入影片路徑
        output_path: 輸出影片路徑（可選）
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

    out = None
    if output_path:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        model_complexity=2,
        enable_segmentation=True,
        smooth_landmarks=True) as pose:

        frame_count = 0
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break

            frame_count += 1

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

                landmarks = results.pose_landmarks.landmark

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

                cv2.putText(image, f"Torso Angle: {torso_angle:.1f}",
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            if results.segmentation_mask is not None:
                condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
                bg_image = np.zeros(image.shape, dtype=np.uint8)
                bg_image[:] = (0, 0, 50)
                image = np.where(condition, image, bg_image)

            cv2.putText(image, f"Frame: {frame_count}/{total_frames}",
                       (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            cv2.imshow('MediaPipe Pose Detection', image)

            if out:
                out.write(image)

            if cv2.waitKey(5) & 0xFF == 27:
                break

            if frame_count % 30 == 0:
                print(f"處理進度: {frame_count}/{total_frames} ({frame_count*100/total_frames:.1f}%)")

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
        print("請確認 video 資料夾存在並包含影片檔案")
        return

    video_files = [f for f in os.listdir(video_folder)
                   if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]

    if not video_files:
        print(f"在 {video_folder} 中找不到影片檔案")
        return

    print(f"找到 {len(video_files)} 個影片檔案:")
    for i, file in enumerate(video_files):
        print(f"  {i+1}. {file}")

    if len(video_files) == 1:
        selected_file = video_files[0]
        print(f"\n自動選擇: {selected_file}")
    else:
        try:
            choice = int(input(f"\n請選擇要處理的影片 (1-{len(video_files)}): "))
            if 1 <= choice <= len(video_files):
                selected_file = video_files[choice - 1]
            else:
                print("無效的選擇")
                return
        except ValueError:
            print("無效的輸入")
            return

    input_path = os.path.join(video_folder, selected_file)

    save_output = input("\n是否儲存處理後的影片? (y/n): ").lower() == 'y'

    output_path = None
    if save_output:
        output_folder = "output"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        output_filename = f"pose_{selected_file}"
        output_path = os.path.join(output_folder, output_filename)
        print(f"輸出檔案將儲存至: {output_path}")

    print("\n開始處理影片...")
    print("按 ESC 鍵可提前結束處理")

    process_video(input_path, output_path)

if __name__ == "__main__":
    main()