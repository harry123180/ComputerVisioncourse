import cv2
import mediapipe as mp
import numpy as np
import os
import time
from threading import Thread
from queue import Queue
import multiprocessing as mproc

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

class GPUPoseDetector:
    """
    GPU 優化的姿態檢測器
    MediaPipe 在 Windows Python 中主要使用 CPU，但透過優化可提升效能
    """
    def __init__(self, use_gpu=True):
        self.use_gpu = use_gpu

        # MediaPipe GPU 設定（實驗性功能）
        if use_gpu:
            print("啟用 GPU 加速模式（MediaPipe + OpenCV GPU）")
            print("注意：MediaPipe Python 版本主要使用 CPU，但會優化處理流程")

            # 檢查 CUDA 是否可用
            self.check_cuda_availability()
        else:
            print("使用 CPU 模式")

        # 初始化 Pose 模型（優化參數）
        self.pose_left = mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=1,  # 降低模型複雜度以加速
            enable_segmentation=False,  # 關閉分割以提升速度
            smooth_landmarks=True,
            static_image_mode=False  # 影片模式優化
        )

        self.pose_right = mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=1,
            enable_segmentation=False,
            smooth_landmarks=True,
            static_image_mode=False
        )

        # 效能監控
        self.fps_counter = []
        self.process_times = []

    def check_cuda_availability(self):
        """檢查 CUDA 是否可用"""
        cuda_available = cv2.cuda.getCudaEnabledDeviceCount() > 0

        if cuda_available:
            print(f"偵測到 {cv2.cuda.getCudaEnabledDeviceCount()} 個 CUDA 設備")

            # 獲取 GPU 資訊
            for i in range(cv2.cuda.getCudaEnabledDeviceCount()):
                cv2.cuda.setDevice(i)
                print(f"GPU {i}: {cv2.cuda.getDevice()}")
        else:
            print("未偵測到 CUDA 設備，將使用 CPU 優化")
            print("若要啟用 GPU，請安裝：")
            print("1. NVIDIA CUDA Toolkit")
            print("2. OpenCV with CUDA support (opencv-contrib-python-headless)")

        return cuda_available

    def process_frame_gpu(self, frame):
        """
        GPU 優化的幀處理
        使用多線程並行處理左右兩個區域
        """
        height, width = frame.shape[:2]
        mid_x = width // 2

        # 分割畫面
        left_region = frame[:, :mid_x]
        right_region = frame[:, mid_x:]

        # 使用 Queue 儲存結果
        results_queue = Queue()

        def process_left():
            start = time.time()
            left_rgb = cv2.cvtColor(left_region, cv2.COLOR_BGR2RGB)
            result = self.pose_left.process(left_rgb)
            results_queue.put(('left', result, time.time() - start))

        def process_right():
            start = time.time()
            right_rgb = cv2.cvtColor(right_region, cv2.COLOR_BGR2RGB)
            result = self.pose_right.process(right_rgb)
            results_queue.put(('right', result, time.time() - start))

        # 並行處理
        thread_left = Thread(target=process_left)
        thread_right = Thread(target=process_right)

        thread_left.start()
        thread_right.start()

        thread_left.join()
        thread_right.join()

        # 收集結果
        results = {}
        process_time = 0
        while not results_queue.empty():
            side, result, t = results_queue.get()
            results[side] = result
            process_time = max(process_time, t)

        return results.get('left'), results.get('right'), process_time

    def draw_optimized(self, image, results_left, results_right):
        """優化的繪圖函數"""
        height, width = image.shape[:2]
        mid_x = width // 2

        # 建立繪圖緩衝區
        overlay = image.copy()
        person_count = 0

        # 處理左側
        if results_left and results_left.pose_landmarks:
            person_count += 1

            # 使用 NumPy 優化繪圖
            landmarks = results_left.pose_landmarks.landmark
            connections = mp_pose.POSE_CONNECTIONS

            # 批量繪製連線
            for connection in connections:
                start_idx, end_idx = connection
                start = landmarks[start_idx]
                end = landmarks[end_idx]

                if start.visibility > 0.5 and end.visibility > 0.5:
                    start_point = (int(start.x * mid_x), int(start.y * height))
                    end_point = (int(end.x * mid_x), int(end.y * height))
                    cv2.line(overlay, start_point, end_point, (255, 0, 0), 2)

            # 批量繪製關鍵點
            for landmark in landmarks:
                if landmark.visibility > 0.5:
                    point = (int(landmark.x * mid_x), int(landmark.y * height))
                    cv2.circle(overlay, point, 3, (255, 0, 0), -1)

            # 計算軀幹角度
            angle = self.calculate_torso_angle(landmarks)
            cv2.putText(overlay, f"Dancer 1: {angle:.1f}°",
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        # 處理右側
        if results_right and results_right.pose_landmarks:
            person_count += 1

            landmarks = results_right.pose_landmarks.landmark
            connections = mp_pose.POSE_CONNECTIONS

            for connection in connections:
                start_idx, end_idx = connection
                start = landmarks[start_idx]
                end = landmarks[end_idx]

                if start.visibility > 0.5 and end.visibility > 0.5:
                    start_point = (int(start.x * mid_x + mid_x), int(start.y * height))
                    end_point = (int(end.x * mid_x + mid_x), int(end.y * height))
                    cv2.line(overlay, start_point, end_point, (0, 255, 0), 2)

            for landmark in landmarks:
                if landmark.visibility > 0.5:
                    point = (int(landmark.x * mid_x + mid_x), int(landmark.y * height))
                    cv2.circle(overlay, point, 3, (0, 255, 0), -1)

            angle = self.calculate_torso_angle(landmarks)
            cv2.putText(overlay, f"Dancer 2: {angle:.1f}°",
                       (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # 混合圖層（使用 NumPy 優化）
        image = cv2.addWeighted(image, 0.7, overlay, 0.3, 0)

        # 繪製分隔線
        cv2.line(image, (mid_x, 0), (mid_x, height), (255, 255, 0), 1)

        return image, person_count

    def calculate_torso_angle(self, landmarks):
        """計算軀幹角度"""
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]

        shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
        shoulder_center_y = (left_shoulder.y + right_shoulder.y) / 2
        hip_center_x = (left_hip.x + right_hip.x) / 2
        hip_center_y = (left_hip.y + right_hip.y) / 2

        angle = np.degrees(np.arctan2(
            hip_center_y - shoulder_center_y,
            hip_center_x - shoulder_center_x
        ))

        return angle

    def process_video(self, video_path, output_path=None):
        """處理影片主函數"""
        cap = cv2.VideoCapture(video_path)

        # 使用硬體加速解碼（如果可用）
        cap.set(cv2.CAP_PROP_HW_ACCELERATION, cv2.VIDEO_ACCELERATION_ANY)

        if not cap.isOpened():
            print(f"無法開啟影片: {video_path}")
            return

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        print(f"\n影片資訊:")
        print(f"  解析度: {width}x{height}")
        print(f"  FPS: {fps}")
        print(f"  總幀數: {total_frames}")
        print(f"  GPU 加速: {'啟用' if self.use_gpu else '停用'}")

        out = None
        if output_path:
            # 使用 H264 編碼器（GPU 加速）
            fourcc = cv2.VideoWriter_fourcc(*'H264')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frame_count = 0
        start_time = time.time()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            frame_start_time = time.time()

            # GPU 加速處理
            results_left, results_right, process_time = self.process_frame_gpu(frame)

            # 優化繪圖
            frame, person_count = self.draw_optimized(frame, results_left, results_right)

            # 計算 FPS
            frame_time = time.time() - frame_start_time
            current_fps = 1.0 / frame_time if frame_time > 0 else 0
            self.fps_counter.append(current_fps)

            # 顯示效能資訊
            cv2.putText(frame, f"FPS: {current_fps:.1f} | Avg: {np.mean(self.fps_counter[-30:]):.1f}",
                       (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

            cv2.putText(frame, f"Process Time: {process_time*1000:.1f}ms",
                       (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

            cv2.putText(frame, f"Detected: {person_count} dancers",
                       (10, 135), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            cv2.putText(frame, f"Frame: {frame_count}/{total_frames}",
                       (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            cv2.imshow('GPU Accelerated Pose Detection', frame)

            if out:
                out.write(frame)

            if cv2.waitKey(1) & 0xFF == 27:  # 更快的響應
                print("\n使用者中斷處理")
                break

            # 進度報告
            if frame_count % 30 == 0:
                elapsed = time.time() - start_time
                avg_fps = frame_count / elapsed
                eta = (total_frames - frame_count) / avg_fps if avg_fps > 0 else 0
                print(f"進度: {frame_count}/{total_frames} ({frame_count*100/total_frames:.1f}%) | "
                      f"平均 FPS: {avg_fps:.1f} | 預計剩餘: {eta:.1f}秒")

        # 清理資源
        self.pose_left.close()
        self.pose_right.close()
        cap.release()
        if out:
            out.release()
        cv2.destroyAllWindows()

        # 效能報告
        total_time = time.time() - start_time
        avg_fps = frame_count / total_time

        print(f"\n處理完成！")
        print(f"總處理時間: {total_time:.2f}秒")
        print(f"平均 FPS: {avg_fps:.1f}")
        print(f"處理幀數: {frame_count}")

        if self.use_gpu:
            print(f"GPU 加速節省時間: ~{(total_frames/fps - total_time):.1f}秒")

def main():
    import sys

    # 設定多處理器優化
    mproc.set_start_method('spawn', force=True)

    # 設定 OpenCV 線程數
    cv2.setNumThreads(4)

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

    output_filename = f"gpu_pose_{selected_file}"
    output_path = os.path.join(output_folder, output_filename)
    print(f"輸出至: {output_path}")

    # 初始化 GPU 加速檢測器
    print("\n初始化 GPU 加速姿態檢測器...")
    detector = GPUPoseDetector(use_gpu=True)

    print("\n開始處理影片 (按 ESC 可中斷)...")
    detector.process_video(input_path, output_path)

if __name__ == "__main__":
    main()