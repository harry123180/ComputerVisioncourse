import cv2
import customtkinter as ctk
import numpy as np
import os
import threading
from PIL import Image, ImageTk

class WebcamApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("單一輪廓裁剪工具")
        self.geometry("800x600")
        
        # UI元件設定
        self.camera_frame = ctk.CTkFrame(self)
        self.camera_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.camera_label = ctk.CTkLabel(self.camera_frame, text="")
        self.camera_label.pack(fill="both", expand=True)

        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.pack(pady=10, padx=10, fill="x")

        # 新增模式切換下拉選單
        self.mode_label = ctk.CTkLabel(self.control_frame, text="顯示模式:")
        self.mode_label.pack(side="left", padx=(10, 5))
        self.mode_option = ctk.CTkOptionMenu(self.control_frame, 
                                             values=["原始圖", "灰階", "模糊化", "Canny", "處理結果"])
        self.mode_option.set("處理結果") # 預設顯示處理結果
        self.mode_option.pack(side="left", padx=5)

        self.option_menu = ctk.CTkOptionMenu(self.control_frame, values=["正面(Front)", "反面(Back)"])
        self.option_menu.pack(side="left", padx=5)

        self.save_button = ctk.CTkButton(self.control_frame, text="拍照並儲存", command=self.save_image)
        self.save_button.pack(side="left", padx=5)

        self.status_label = ctk.CTkLabel(self.control_frame, text="狀態：準備就緒")
        self.status_label.pack(side="left", padx=5)
        
        # 影像處理變數
        self.cap = None
        self.current_frame = None
        self.cropped_image = None
        self.is_running = True
        self.file_counter = 1
        
        # 啟動攝影機串流
        self.camera_thread = threading.Thread(target=self.start_camera_stream)
        self.camera_thread.daemon = True
        self.camera_thread.start()

    def start_camera_stream(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.status_label.configure(text="錯誤：無法開啟Webcam")
            return

        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            self.current_frame = frame.copy()
            
            display_frame, cropped_image = self.process_and_display(frame)
            self.cropped_image = cropped_image
            
            img_pil = Image.fromarray(cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB))
            img_tk = ImageTk.PhotoImage(image=img_pil)
            self.camera_label.configure(image=img_tk)
            self.camera_label.image = img_tk
            
            self.update()

    def process_and_display(self, frame):
        # 影像處理階段
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 30, 90) # 使用較寬鬆的Canny條件
        
        mode = self.mode_option.get()

        if mode == "灰階":
            return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR), None
        elif mode == "模糊化":
            return cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR), None
        elif mode == "Canny":
            return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR), None
        elif mode == "原始圖":
            return frame, None
        
        # 處理結果模式：尋找輪廓、繪製、裁剪
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 顯示所有符合面積範圍的輪廓的面積
        cropped_image = None
        main_contour = None
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if 500 <= area <= 1500:
                # 繪製符合條件的輪廓
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
                
                # 計算中心點並顯示面積
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    
                    # 顯示面積值
                    text_x = cX + 10
                    text_y = cY + 10
                    cv2.putText(frame, f"Area: {int(area)}", (text_x, text_y), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

                    # 如果這是唯一的輪廓，則進行裁剪
                    if main_contour is None:
                        main_contour = contour
                    else:
                        main_contour = None # 如果有多個輪廓，則不進行裁剪
        
        if main_contour is not None:
            # 繪製中心點
            M = cv2.moments(main_contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)

            # 裁剪224x224矩形區域
            half_size = 112
            height, width, _ = frame.shape
            
            x1 = max(0, cX - half_size)
            y1 = max(0, cY - half_size)
            x2 = min(width, cX + half_size)
            y2 = min(height, cY + half_size)
            
            if x2 - x1 < 224:
                if x1 == 0:
                    x2 = min(width, 224)
                elif x2 == width:
                    x1 = max(0, width - 224)
            
            if y2 - y1 < 224:
                if y1 == 0:
                    y2 = min(height, 224)
                elif y2 == height:
                    y1 = max(0, height - 224)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cropped_image = self.current_frame[y1:y2, x1:x2]

        return frame, cropped_image

    def save_image(self):
        if self.cropped_image is not None and self.cropped_image.shape[0] == 224 and self.cropped_image.shape[1] == 224:
            side = self.option_menu.get().split('(')[0].strip().lower()
            
            while True:
                filename = f"{self.file_counter}.jpg"
                if not os.path.exists(filename):
                    break
                self.file_counter += 1
            
            cv2.imwrite(filename, self.cropped_image)
            self.status_label.configure(text=f"儲存成功：{filename} ({side})")
            print(f"圖片已儲存為 {filename}")
        else:
            self.status_label.configure(text="錯誤：沒有偵測到單一輪廓或無法裁剪")

    def on_closing(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
        self.destroy()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = WebcamApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()