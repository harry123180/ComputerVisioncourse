import customtkinter as ctk
import cv2
import numpy as np
from PIL import Image, ImageTk
import os
from threading import Thread, Event
import time

class ContourCaptureApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("輪廓擷取工具")
        self.root.geometry("900x700")
        
        # 設定主題
        ctk.set_appearance_mode("light")
        
        # 相機相關
        self.cap = None
        self.is_running = False
        self.current_frame = None
        self.processed_frame = None
        self.roi_frame = None
        self.contour_center = None
        self.roi_rect = None
        
        # 資料夾設定
        self.mode = "Front"
        self.create_directories()
        
        # 建立UI
        self.setup_ui()
        
        # 啟動相機
        self.start_camera()
        
    def create_directories(self):
        """創建training_data/Front和training_data/Back資料夾"""
        os.makedirs("training_data/Front", exist_ok=True)
        os.makedirs("training_data/Back", exist_ok=True)
        
    def get_next_filename(self, folder):
        """取得下一個可用的檔案編號"""
        existing_files = [f for f in os.listdir(folder) if f.endswith('.jpg')]
        if not existing_files:
            return "1.jpg"
        
        numbers = []
        for f in existing_files:
            try:
                num = int(f.replace('.jpg', ''))
                numbers.append(num)
            except:
                continue
        
        if numbers:
            return f"{max(numbers) + 1}.jpg"
        return "1.jpg"
        
    def setup_ui(self):
        """建立使用者介面"""
        # 主要框架
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 控制面板
        control_frame = ctk.CTkFrame(main_frame)
        control_frame.pack(fill="x", padx=5, pady=5)
        
        # Front/Back 選擇
        mode_label = ctk.CTkLabel(control_frame, text="模式選擇:", font=("Arial", 14))
        mode_label.pack(side="left", padx=10)
        
        self.mode_var = ctk.StringVar(value="Front")
        mode_menu = ctk.CTkSegmentedButton(
            control_frame,
            values=["Front", "Back"],
            variable=self.mode_var,
            command=self.on_mode_change
        )
        mode_menu.pack(side="left", padx=10)
        
        # 拍照按鈕
        self.capture_btn = ctk.CTkButton(
            control_frame,
            text="拍照存檔",
            command=self.capture_image,
            width=120,
            height=35,
            font=("Arial", 14, "bold")
        )
        self.capture_btn.pack(side="left", padx=20)
        
        # 狀態顯示
        self.status_label = ctk.CTkLabel(
            control_frame,
            text="準備就緒",
            font=("Arial", 12)
        )
        self.status_label.pack(side="left", padx=10)
        
        # 參數調整框架
        param_frame = ctk.CTkFrame(main_frame)
        param_frame.pack(fill="x", padx=5, pady=5)
        
        # Canny閾值調整
        canny_label = ctk.CTkLabel(param_frame, text="Canny閾值:", font=("Arial", 12))
        canny_label.pack(side="left", padx=10)
        
        self.canny_low = ctk.CTkSlider(
            param_frame,
            from_=0,
            to=200,
            number_of_steps=200,
            command=self.update_canny
        )
        self.canny_low.set(50)
        self.canny_low.pack(side="left", padx=5)
        
        self.canny_low_label = ctk.CTkLabel(param_frame, text="Low: 50", font=("Arial", 10))
        self.canny_low_label.pack(side="left", padx=5)
        
        self.canny_high = ctk.CTkSlider(
            param_frame,
            from_=0,
            to=300,
            number_of_steps=300,
            command=self.update_canny
        )
        self.canny_high.set(150)
        self.canny_high.pack(side="left", padx=5)
        
        self.canny_high_label = ctk.CTkLabel(param_frame, text="High: 150", font=("Arial", 10))
        self.canny_high_label.pack(side="left", padx=5)
        
        # 影像顯示區域
        display_frame = ctk.CTkFrame(main_frame)
        display_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 原始影像
        original_frame = ctk.CTkFrame(display_frame)
        original_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        ctk.CTkLabel(original_frame, text="即時預覽", font=("Arial", 14, "bold")).pack()
        self.original_label = ctk.CTkLabel(original_frame, text="")
        self.original_label.pack(fill="both", expand=True)
        
        # 處理後影像
        processed_frame = ctk.CTkFrame(display_frame)
        processed_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        ctk.CTkLabel(processed_frame, text="輪廓檢測", font=("Arial", 14, "bold")).pack()
        self.processed_label = ctk.CTkLabel(processed_frame, text="")
        self.processed_label.pack(fill="both", expand=True)
        
        # ROI影像
        roi_frame = ctk.CTkFrame(display_frame)
        roi_frame.pack(side="left", padx=5)
        
        ctk.CTkLabel(roi_frame, text="224x224 ROI", font=("Arial", 14, "bold")).pack()
        self.roi_label = ctk.CTkLabel(roi_frame, text="")
        self.roi_label.pack()
        
    def update_canny(self, value):
        """更新Canny閾值顯示"""
        low_val = int(self.canny_low.get())
        high_val = int(self.canny_high.get())
        self.canny_low_label.configure(text=f"Low: {low_val}")
        self.canny_high_label.configure(text=f"High: {high_val}")
        
    def on_mode_change(self, value):
        """模式切換"""
        self.mode = value
        self.status_label.configure(text=f"切換至 {value} 模式")
        
    def start_camera(self):
        """啟動相機"""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.status_label.configure(text="相機開啟失敗")
            return
            
        self.is_running = True
        self.camera_thread = Thread(target=self.update_camera, daemon=True)
        self.camera_thread.start()
        
    def process_frame(self, frame):
        """處理影像框架"""
        # 轉換為灰階
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 高斯模糊
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Canny邊緣檢測
        low_threshold = int(self.canny_low.get())
        high_threshold = int(self.canny_high.get())
        edges = cv2.Canny(blurred, low_threshold, high_threshold)
        
        # 尋找輪廓
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 建立顯示用影像
        display_frame = frame.copy()
        roi_frame = None
        
        if contours:
            # 找最大輪廓
            largest_contour = max(contours, key=cv2.contourArea)
            
            # 計算輪廓中心
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                self.contour_center = (cx, cy)
                
                # 繪製輪廓
                cv2.drawContours(display_frame, [largest_contour], -1, (0, 255, 0), 2)
                
                # 繪製中心點
                cv2.circle(display_frame, (cx, cy), 5, (0, 0, 255), -1)
                
                # 計算224x224的ROI區域
                h, w = frame.shape[:2]
                half_size = 112
                
                # 確保ROI在影像範圍內
                x1 = max(0, cx - half_size)
                y1 = max(0, cy - half_size)
                x2 = min(w, x1 + 224)
                y2 = min(h, y1 + 224)
                
                # 調整起始點以確保224x224
                if x2 - x1 < 224:
                    x1 = max(0, x2 - 224)
                if y2 - y1 < 224:
                    y1 = max(0, y2 - 224)
                
                self.roi_rect = (x1, y1, x2, y2)
                
                # 繪製ROI矩形
                cv2.rectangle(display_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                
                # 擷取ROI區域
                roi_frame = frame[y1:y2, x1:x2]
                
                # 確保ROI是224x224
                if roi_frame.shape[:2] != (224, 224):
                    roi_frame = cv2.resize(roi_frame, (224, 224))
                
                self.roi_frame = roi_frame
            else:
                self.contour_center = None
                self.roi_rect = None
                self.roi_frame = None
        else:
            self.contour_center = None
            self.roi_rect = None
            self.roi_frame = None
            
        return display_frame, edges, roi_frame
        
    def update_camera(self):
        """相機更新迴圈"""
        while self.is_running:
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame
                
                # 處理影像
                display_frame, edges, roi_frame = self.process_frame(frame)
                self.processed_frame = display_frame
                
                # 更新原始影像顯示
                img = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                img = img.resize((400, 300), Image.Resampling.LANCZOS)
                imgtk = ImageTk.PhotoImage(image=img)
                self.original_label.configure(image=imgtk)
                self.original_label.image = imgtk
                
                # 更新邊緣檢測顯示
                edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
                img_edges = Image.fromarray(edges_rgb)
                img_edges = img_edges.resize((400, 300), Image.Resampling.LANCZOS)
                imgtk_edges = ImageTk.PhotoImage(image=img_edges)
                self.processed_label.configure(image=imgtk_edges)
                self.processed_label.image = imgtk_edges
                
                # 更新ROI顯示
                if roi_frame is not None:
                    roi_rgb = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2RGB)
                    img_roi = Image.fromarray(roi_rgb)
                    imgtk_roi = ImageTk.PhotoImage(image=img_roi)
                    self.roi_label.configure(image=imgtk_roi)
                    self.roi_label.image = imgtk_roi
                else:
                    self.roi_label.configure(image="")
                    
            time.sleep(0.03)  # ~30 FPS
            
    def capture_image(self):
        """拍照並儲存"""
        if self.roi_frame is not None:
            folder = f"training_data/{self.mode}"
            filename = self.get_next_filename(folder)
            filepath = os.path.join(folder, filename)
            
            # 儲存224x224的ROI影像
            cv2.imwrite(filepath, self.roi_frame)
            
            self.status_label.configure(
                text=f"已儲存至 {filepath}"
            )
        else:
            self.status_label.configure(
                text="未偵測到輪廓，無法儲存"
            )
            
    def on_closing(self):
        """關閉應用程式"""
        self.is_running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()
        
    def run(self):
        """執行應用程式"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

if __name__ == "__main__":
    app = ContourCaptureApp()
    app.run()