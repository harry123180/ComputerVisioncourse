import cv2
import mediapipe as mp
import numpy as np
import os
import time
from collections import deque
import math

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

class SquatAnalyzer:
    """
    深蹲姿勢分析器
    分析側面拍攝的深蹲影片，計算關節角度並評估動作品質
    """

    def __init__(self):
        # 初始化 MediaPipe Pose
        self.pose = mp_pose.Pose(
            min_detection_confidence=0.7,  # 提高信心閾值
            min_tracking_confidence=0.7,
            model_complexity=2,  # 使用最精確的模型
            enable_segmentation=False,
            smooth_landmarks=True,
            static_image_mode=False
        )

        # 深蹲狀態追蹤
        self.squat_count = 0
        self.stage = "up"  # up 或 down
        self.form_feedback = []

        # 角度歷史記錄（用於平滑處理）
        self.knee_angles_history = deque(maxlen=5)
        self.hip_angles_history = deque(maxlen=5)
        self.back_angles_history = deque(maxlen=5)

        # 深蹲品質指標
        self.good_reps = 0
        self.bad_reps = 0

        # 時間追蹤
        self.rep_times = []
        self.last_rep_time = None

    def calculate_angle(self, a, b, c):
        """
        計算三個點形成的角度
        a, b, c: 三個關節點，b 是頂點
        """
        a = np.array([a.x, a.y])
        b = np.array([b.x, b.y])
        c = np.array([c.x, c.y])

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
                  np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle

    def smooth_angle(self, angle, history_deque):
        """
        使用移動平均平滑角度數據
        """
        history_deque.append(angle)
        if len(history_deque) > 0:
            return np.mean(history_deque)
        return angle

    def check_form(self, knee_angle, hip_angle, back_angle, depth):
        """
        評估深蹲姿勢品質
        """
        feedback = []
        score = 100

        # 檢查深度（理想深蹲膝蓋角度 < 90度）
        if depth == "down":
            if knee_angle > 110:
                feedback.append("Insufficient depth - Go lower")
                score -= 30
            elif knee_angle < 70:
                feedback.append("Too deep - May stress knees")
                score -= 10

        # 檢查膝蓋位置（膝蓋不應過度前傾）
        if knee_angle < 80 and depth == "down":
            if hip_angle < 70:
                feedback.append("Knees too far forward")
                score -= 20

        # 檢查背部角度（應保持相對直立）
        if back_angle < 145:  # 背部過度彎曲
            feedback.append("Keep back straight")
            score -= 25
        elif back_angle > 175:  # 過度後仰
            feedback.append("Avoid excessive lean back")
            score -= 15

        # 綜合評分
        if score >= 80:
            form_quality = "Excellent"
            color = (0, 255, 0)
        elif score >= 60:
            form_quality = "Good"
            color = (0, 255, 255)
        else:
            form_quality = "Needs Work"
            color = (0, 0, 255)

        return form_quality, feedback, score, color

    def detect_rep(self, knee_angle):
        """
        偵測深蹲次數
        """
        rep_completed = False

        # 下蹲階段
        if knee_angle < 100 and self.stage == "up":
            self.stage = "down"

        # 起身階段
        elif knee_angle > 140 and self.stage == "down":
            self.stage = "up"
            self.squat_count += 1
            rep_completed = True

            # 記錄時間
            current_time = time.time()
            if self.last_rep_time:
                rep_duration = current_time - self.last_rep_time
                self.rep_times.append(rep_duration)
            self.last_rep_time = current_time

        return rep_completed

    def process_frame(self, image):
        """
        處理單幀影像
        """
        # 轉換色彩空間
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # 獲取關鍵關節點（使用左側，因為是側面拍攝）
            # 如果左側不可見，使用右側
            if landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].visibility > 0.5:
                hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
                knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
                ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
                shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
                ear = landmarks[mp_pose.PoseLandmark.LEFT_EAR.value]
            else:
                hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
                knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
                ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
                shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
                ear = landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value]

            # 計算角度
            knee_angle_raw = self.calculate_angle(hip, knee, ankle)
            hip_angle_raw = self.calculate_angle(shoulder, hip, knee)
            back_angle_raw = self.calculate_angle(ear, shoulder, hip)

            # 平滑角度
            knee_angle = self.smooth_angle(knee_angle_raw, self.knee_angles_history)
            hip_angle = self.smooth_angle(hip_angle_raw, self.hip_angles_history)
            back_angle = self.smooth_angle(back_angle_raw, self.back_angles_history)

            # 偵測深蹲次數
            rep_completed = self.detect_rep(knee_angle)

            # 評估姿勢
            form_quality, feedback, score, color = self.check_form(
                knee_angle, hip_angle, back_angle, self.stage
            )

            if rep_completed:
                if score >= 60:
                    self.good_reps += 1
                else:
                    self.bad_reps += 1

            return {
                'landmarks': results.pose_landmarks,
                'knee_angle': knee_angle,
                'hip_angle': hip_angle,
                'back_angle': back_angle,
                'stage': self.stage,
                'count': self.squat_count,
                'form_quality': form_quality,
                'feedback': feedback,
                'score': score,
                'color': color,
                'good_reps': self.good_reps,
                'bad_reps': self.bad_reps
            }

        return None

    def draw_analysis(self, image, analysis_data):
        """
        在影像上繪製分析結果
        """
        height, width = image.shape[:2]

        if analysis_data:
            # 繪製骨架
            mp_drawing.draw_landmarks(
                image,
                analysis_data['landmarks'],
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(
                    color=analysis_data['color'], thickness=2, circle_radius=3
                ),
                connection_drawing_spec=mp_drawing.DrawingSpec(
                    color=analysis_data['color'], thickness=2, circle_radius=2
                )
            )

            # 建立資訊面板背景
            overlay = image.copy()
            cv2.rectangle(overlay, (10, 10), (400, 250), (0, 0, 0), -1)
            image = cv2.addWeighted(image, 0.7, overlay, 0.3, 0)

            # 顯示深蹲次數
            cv2.putText(image, f"Squat Count: {analysis_data['count']}",
                       (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

            # 顯示良好/需改進次數
            cv2.putText(image, f"Good: {analysis_data['good_reps']} | Bad: {analysis_data['bad_reps']}",
                       (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # 顯示當前狀態
            stage_color = (0, 255, 0) if analysis_data['stage'] == "up" else (0, 165, 255)
            cv2.putText(image, f"Stage: {analysis_data['stage'].upper()}",
                       (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, stage_color, 2)

            # 顯示角度
            cv2.putText(image, f"Knee: {analysis_data['knee_angle']:.1f}°",
                       (20, 145), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(image, f"Hip: {analysis_data['hip_angle']:.1f}°",
                       (150, 145), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(image, f"Back: {analysis_data['back_angle']:.1f}°",
                       (260, 145), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # 顯示姿勢品質
            cv2.putText(image, f"Form: {analysis_data['form_quality']}",
                       (20, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                       analysis_data['color'], 2)

            # 顯示評分
            cv2.putText(image, f"Score: {analysis_data['score']}/100",
                       (20, 215), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                       analysis_data['color'], 2)

            # 顯示回饋（右側）
            if analysis_data['feedback']:
                feedback_y = 40
                for feedback in analysis_data['feedback']:
                    cv2.putText(image, feedback,
                               (width - 350, feedback_y),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                               (0, 0, 255), 2)
                    feedback_y += 30

            # 繪製角度弧線（膝蓋）
            if analysis_data['landmarks']:
                landmarks = analysis_data['landmarks'].landmark
                if landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].visibility > 0.5:
                    knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
                else:
                    knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]

                knee_x = int(knee.x * width)
                knee_y = int(knee.y * height)

                # 繪製角度指示器
                cv2.ellipse(image, (knee_x, knee_y), (50, 50), 0,
                           -90, -90 + analysis_data['knee_angle'],
                           (0, 255, 255), 2)

        return image

def process_squat_video(video_path, output_path=None):
    """
    處理深蹲影片
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Cannot open video: {video_path}")
        return

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"Video Info:")
    print(f"  Resolution: {width}x{height}")
    print(f"  FPS: {fps}")
    print(f"  Total frames: {total_frames}")
    print(f"  Mode: Squat Analysis")

    out = None
    if output_path:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # 初始化分析器
    analyzer = SquatAnalyzer()

    frame_count = 0
    start_time = time.time()

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame_count += 1

        # 分析姿勢
        analysis_data = analyzer.process_frame(frame)

        # 繪製結果
        frame = analyzer.draw_analysis(frame, analysis_data)

        # 顯示進度
        cv2.putText(frame, f"Frame: {frame_count}/{total_frames}",
                   (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX,
                   0.7, (255, 255, 255), 2)

        # 顯示 FPS
        elapsed = time.time() - start_time
        if elapsed > 0:
            current_fps = frame_count / elapsed
            cv2.putText(frame, f"FPS: {current_fps:.1f}",
                       (width - 120, height - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow('Squat Analysis', frame)

        if out:
            out.write(frame)

        if cv2.waitKey(1) & 0xFF == 27:
            print("\nUser interrupted")
            break

        # 進度報告
        if frame_count % 30 == 0:
            print(f"Progress: {frame_count}/{total_frames} ({frame_count*100/total_frames:.1f}%)")
            if analyzer.squat_count > 0:
                print(f"  Squat count: {analyzer.squat_count}")
                print(f"  Good: {analyzer.good_reps} | Needs work: {analyzer.bad_reps}")

    # 清理資源
    analyzer.pose.close()
    cap.release()
    if out:
        out.release()
    cv2.destroyAllWindows()

    # 顯示最終統計
    total_time = time.time() - start_time
    print(f"\n=== Analysis Complete ===")
    print(f"Total processing time: {total_time:.2f}s")
    print(f"Total squats: {analyzer.squat_count}")
    print(f"Good form: {analyzer.good_reps}")
    print(f"Needs improvement: {analyzer.bad_reps}")

    if analyzer.good_reps > 0:
        accuracy = (analyzer.good_reps / analyzer.squat_count) * 100
        print(f"Form accuracy: {accuracy:.1f}%")

    if len(analyzer.rep_times) > 0:
        avg_rep_time = np.mean(analyzer.rep_times)
        print(f"Average rep time: {avg_rep_time:.2f}s")

def main():
    import sys

    # 尋找 example.mp4
    video_path = None

    # 優先尋找 example.mp4
    if os.path.exists("example.mp4"):
        video_path = "example.mp4"
    elif os.path.exists("../example.mp4"):
        video_path = "../example.mp4"
    elif os.path.exists("../video/example.mp4"):
        video_path = "../video/example.mp4"
    else:
        # 如果找不到 example.mp4，尋找 video 資料夾
        if len(sys.argv) > 1:
            video_folder = sys.argv[1]
        else:
            video_folder = "../video"
            if not os.path.exists(video_folder):
                video_folder = "video"
            if not os.path.exists(video_folder):
                video_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "video")

        if os.path.exists(video_folder):
            video_files = [f for f in os.listdir(video_folder)
                          if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]

            # 優先選擇 example.mp4
            for file in video_files:
                if 'example' in file.lower() or 'squat' in file.lower():
                    video_path = os.path.join(video_folder, file)
                    break

            # 如果還是找不到，使用第一個影片
            if not video_path and video_files:
                video_path = os.path.join(video_folder, video_files[0])

    if not video_path:
        print("Video file not found")
        print("Please name your squat video as example.mp4 and place it in DAY2 or video folder")
        return

    print(f"Processing video: {video_path}")

    # 設定輸出路徑
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_filename = f"squat_analysis_{os.path.basename(video_path)}"
    output_path = os.path.join(output_folder, output_filename)
    print(f"Output to: {output_path}")

    print("\nStarting squat analysis (Press ESC to stop)...")
    process_squat_video(video_path, output_path)

if __name__ == "__main__":
    main()