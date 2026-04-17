"""Day 1 Step 07: 雙攝影機 + Mediapipe (FaceMesh & Pose)"""
import cv2
import numpy as np
import mediapipe as mp

# Author: harry123180


def main() -> None:
    """Camera 0: FaceMesh 臉部網格 / Camera 1: Pose 姿勢骨架"""

    # 初始化 Mediapipe 模組
    mp_face_mesh = mp.solutions.face_mesh
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    # 建立 FaceMesh 和 Pose 偵測器
    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,  # 包含眼睛和嘴唇細節
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    pose = mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    # 開啟兩個攝影機 (0=內建, 1=外接)
    camera_0 = cv2.VideoCapture(0)
    camera_1 = cv2.VideoCapture(1)

    # 檢查攝影機是否成功開啟
    if not camera_0.isOpened():
        print("錯誤：無法開啟攝影機 0 (內建)")
        return
    if not camera_1.isOpened():
        print("錯誤：無法開啟攝影機 1 (外接)")
        camera_0.release()
        return

    print("=" * 50)
    print("雙攝影機 + Mediapipe 已啟動")
    print("Camera 0: FaceMesh 臉部網格偵測")
    print("Camera 1: Pose 姿勢骨架偵測")
    print("=" * 50)
    print("按 ESC 關閉程式")
    print("按 'v' 切換垂直/水平排列")

    # 設定統一的畫面大小
    display_width = 640
    display_height = 480

    # 排列模式：True=水平並排, False=垂直堆疊
    horizontal_mode = True

    while True:
        # 讀取兩個攝影機的畫面
        success_0, frame_0 = camera_0.read()
        success_1, frame_1 = camera_1.read()

        # 如果任一攝影機讀取失敗就跳出
        if not success_0 or not success_1:
            print("攝影機讀取失敗")
            break

        # 統一縮放到相同尺寸
        frame_0 = cv2.resize(frame_0, (display_width, display_height))
        frame_1 = cv2.resize(frame_1, (display_width, display_height))

        # ===== Camera 0: FaceMesh 處理 =====
        # 轉換 BGR -> RGB (Mediapipe 需要 RGB)
        rgb_0 = cv2.cvtColor(frame_0, cv2.COLOR_BGR2RGB)
        rgb_0.flags.writeable = False  # 提升效能
        face_results = face_mesh.process(rgb_0)
        rgb_0.flags.writeable = True

        # 繪製 FaceMesh 網格
        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                # 繪製臉部網格
                mp_drawing.draw_landmarks(
                    image=frame_0,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
                )
                # 繪製臉部輪廓
                mp_drawing.draw_landmarks(
                    image=frame_0,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style()
                )
                # 繪製眼睛虹膜
                mp_drawing.draw_landmarks(
                    image=frame_0,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style()
                )

        # ===== Camera 1: Pose 處理 =====
        # 轉換 BGR -> RGB
        rgb_1 = cv2.cvtColor(frame_1, cv2.COLOR_BGR2RGB)
        rgb_1.flags.writeable = False
        pose_results = pose.process(rgb_1)
        rgb_1.flags.writeable = True

        # 繪製 Pose 骨架
        if pose_results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image=frame_1,
                landmark_list=pose_results.pose_landmarks,
                connections=mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
            )

        # 在畫面上加入標籤
        cv2.putText(frame_0, "FaceMesh", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame_1, "Pose", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # 根據模式拼接畫面
        if horizontal_mode:
            # 水平並排 (左右)
            combined = np.hstack([frame_0, frame_1])
        else:
            # 垂直堆疊 (上下)
            combined = np.vstack([frame_0, frame_1])

        # 顯示整合後的畫面
        cv2.imshow("Dual Camera - FaceMesh & Pose", combined)

        # 按鍵處理
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC 離開
            break
        elif key == ord('v'):  # 切換排列模式
            horizontal_mode = not horizontal_mode
            mode_name = "水平並排" if horizontal_mode else "垂直堆疊"
            print(f"切換為: {mode_name}")

    # 釋放資源
    face_mesh.close()
    pose.close()
    camera_0.release()
    camera_1.release()
    cv2.destroyAllWindows()
    print("程式結束")


if __name__ == "__main__":
    main()
