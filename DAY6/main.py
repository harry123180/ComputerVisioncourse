import cv2
import numpy as np
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import threading
import time
import datetime
import os
import json
import math
from ultralytics import YOLO
import sys, os

def resource_path(rel_path: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, rel_path)
# --- Main Application Class (V8) ---
# This version is a major refactor based on the user-provided `smart_vision_tool_v4.py`
# It incorporates the corner-finding logic, calibration, and warpAffine display method from that file.

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- App State ---
        self.is_webcam_running = False
        self.cap = None
        self.original_frame = None
        self.last_results_px = None

        # --- YOLO Model ---
        self.yolo_model = None
        self.yolo_results = None
        try:
            model_path = resource_path("models/best.pt")
            if os.path.exists(model_path):
                self.yolo_model = YOLO(model_path)
                print("YOLO model loaded successfully")
            else:
                print(f"YOLO model not found at {model_path}")
        except Exception as e:
            print(f"Error loading YOLO model: {e}")
            self.yolo_model = None

        # --- Viewport State ---
        self.zoom_level = 1.0
        self.pan_offset = [0, 0]

        # --- Config & Calibration ---
        self.config_file = "config.json" # Store in the same directory
        self.pixel_to_mm_ratio = self.load_config()

        # --- Window Setup ---
        self.title("智慧視覺量測工具 v8")
        self.geometry("1200x750")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- UI Panels ---
        self.left_panel = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.left_panel.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.left_panel.grid_rowconfigure(7, weight=1)

        self.right_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        self.right_panel.grid_rowconfigure(0, weight=1)
        self.right_panel.grid_columnconfigure(0, weight=1)

        self.image_label = ctk.CTkLabel(self.right_panel, text="請從左側選擇模式")
        self.image_label.grid(row=0, column=0, sticky="nsew")

        self.view_controls_frame = ctk.CTkFrame(self)
        self.view_controls_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # --- Left Panel Widgets ---
        ctk.CTkLabel(self.left_panel, text="控制項", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=20, pady=(20, 10))

        self.tab_view = ctk.CTkTabview(self.left_panel)
        self.tab_view.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.tab_view.add("即時影像")
        self.tab_view.add("靜態圖片")

        ctk.CTkButton(self.tab_view.tab("即時影像"), text="開啟攝影機", command=self.start_webcam).pack(pady=5, fill="x")
        ctk.CTkButton(self.tab_view.tab("即時影像"), text="關閉攝影機", command=self.stop_webcam).pack(pady=5, fill="x")
        ctk.CTkButton(self.tab_view.tab("靜態圖片"), text="選擇圖片", command=self.select_image).pack(pady=5, fill="x")

        self.show_measurement_checkbox = ctk.CTkCheckBox(self.left_panel, text="顯示量測結果", command=self.process_and_display_image)
        self.show_measurement_checkbox.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.show_yolo_checkbox = ctk.CTkCheckBox(self.left_panel, text="顯示YOLO辨識", command=self.process_and_display_image)
        self.show_yolo_checkbox.grid(row=3, column=0, padx=20, pady=5, sticky="w")

        self.unit_var = ctk.StringVar(value="pixel")
        ctk.CTkLabel(self.left_panel, text="單位:").grid(row=4, column=0, padx=20, pady=(10, 0), sticky="w")
        ctk.CTkOptionMenu(self.left_panel, values=["pixel", "mm", "inch"], variable=self.unit_var, command=self.update_results_display).grid(row=5, column=0, padx=20, pady=10, sticky="w")

        ctk.CTkButton(self.left_panel, text="校準", command=self.open_calibration_window).grid(row=6, column=0, padx=20, pady=10)

        self.results_frame = ctk.CTkFrame(self.left_panel)
        self.results_frame.grid(row=7, column=0, padx=20, pady=10, sticky="nsew")
        ctk.CTkLabel(self.results_frame, text="量測結果:", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        self.result_text_A = ctk.CTkLabel(self.results_frame, text="A 邊: --")
        self.result_text_A.pack()
        self.result_text_B = ctk.CTkLabel(self.results_frame, text="B 邊: --")
        self.result_text_B.pack()
        self.result_text_C = ctk.CTkLabel(self.results_frame, text="C 邊: --")
        self.result_text_C.pack()
        self.result_text_D = ctk.CTkLabel(self.results_frame, text="D 邊: --")
        self.result_text_D.pack()

        ctk.CTkLabel(self.results_frame, text="", font=ctk.CTkFont(size=2)).pack()
        ctk.CTkLabel(self.results_frame, text="YOLO辨識結果:", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        self.yolo_results_text = ctk.CTkTextbox(self.results_frame, width=250, height=150)
        self.yolo_results_text.pack(pady=5)

        # --- Bottom View Controls ---
        self.view_controls_frame.grid_columnconfigure(0, weight=1)
        self.button_container = ctk.CTkFrame(self.view_controls_frame, fg_color="transparent")
        self.button_container.grid(row=0, column=0)
        ctk.CTkButton(self.button_container, text="放大 (+)", command=lambda: self.zoom(1.2)).pack(side="left", padx=5)
        ctk.CTkButton(self.button_container, text="縮小 (-)", command=lambda: self.zoom(0.8)).pack(side="left", padx=5)
        ctk.CTkButton(self.button_container, text="←", command=lambda: self.pan(-50, 0)).pack(side="left", padx=5)
        ctk.CTkButton(self.button_container, text="↑", command=lambda: self.pan(0, -50)).pack(side="left", padx=5)
        ctk.CTkButton(self.button_container, text="↓", command=lambda: self.pan(0, 50)).pack(side="left", padx=5)
        ctk.CTkButton(self.button_container, text="→", command=lambda: self.pan(50, 0)).pack(side="left", padx=5)
        ctk.CTkButton(self.button_container, text="重置", command=self.reset_view).pack(side="left", padx=5)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    # --- Core Methods ---
    def start_webcam(self):
        if self.is_webcam_running: return
        self.cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            messagebox.showerror("錯誤", "無法開啟攝影機")
            self.cap = None
            return
        self.is_webcam_running = True
        self.reset_view()
        self.update_webcam_feed()

    def stop_webcam(self):
        self.is_webcam_running = False
        if self.cap: self.cap.release(); self.cap = None

    def update_webcam_feed(self):
        if not self.is_webcam_running: return
        ret, frame = self.cap.read()
        if ret:
            self.original_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.process_and_display_image()
        self.after(20, self.update_webcam_feed)

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if not file_path: return
        self.stop_webcam()
        self.original_frame = cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2RGB)
        self.reset_view()
        self.process_and_display_image()

    def process_and_display_image(self):
        if self.original_frame is None:
            self.image_label.configure(image=None, text="請從左側選擇模式")
            return

        display_img = self.original_frame.copy()

        if self.show_measurement_checkbox.get():
            display_img, results = self.measure_image(display_img)
            self.last_results_px = results
        else:
            self.last_results_px = None

        if self.show_yolo_checkbox.get():
            display_img, self.yolo_results = self.perform_yolo_detection(display_img)
            self.update_yolo_results_display()
        else:
            self.yolo_results = None
            self.update_yolo_results_display()

        self.update_results_display()

        # Apply Zoom and Pan using warpAffine
        h, w, _ = display_img.shape
        M = np.float32([[self.zoom_level, 0, self.pan_offset[0]], [0, self.zoom_level, self.pan_offset[1]]])
        display_img = cv2.warpAffine(display_img, M, (w, h))

        # Resize to fit the label while maintaining aspect ratio
        label_w, label_h = self.image_label.winfo_width(), self.image_label.winfo_height()
        if label_w <= 1 or label_h <= 1: self.after(50, self.process_and_display_image); return

        img_aspect = w / h
        label_aspect = label_w / label_h
        if img_aspect > label_aspect:
            new_w, new_h = label_w, int(label_w / img_aspect)
        else:
            new_h, new_w = label_h, int(label_h * img_aspect)
        
        if new_w > 0 and new_h > 0:
            resized_img = cv2.resize(display_img, (new_w, new_h))
            img_pil = Image.fromarray(resized_img)
            ctk_img = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(new_w, new_h))
            self.image_label.configure(image=ctk_img, text="")
        else:
            self.image_label.configure(image=None, text="影像處理錯誤")

    def perform_yolo_detection(self, img):
        """Perform YOLO detection on the image and draw results"""
        if self.yolo_model is None:
            return img, None

        try:
            img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            results = self.yolo_model.predict(source=img_bgr, conf=0.3, verbose=False)

            detection_info = []
            if results and len(results) > 0:
                result = results[0]
                if result.boxes is not None and len(result.boxes) > 0:
                    for box in result.boxes:
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        conf = box.conf[0].cpu().numpy()
                        cls = int(box.cls[0].cpu().numpy())

                        class_name = result.names[cls] if cls in result.names else f"Class_{cls}"

                        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                        label = f"{class_name}: {conf:.2f}"
                        cv2.putText(img, label, (int(x1), int(y1) - 10),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                        detection_info.append({
                            "class": class_name,
                            "confidence": conf,
                            "bbox": [x1, y1, x2, y2]
                        })

            return img, detection_info

        except Exception as e:
            print(f"Error during YOLO detection: {e}")
            return img, None

    def measure_image(self, img):
        """ Adopts the logic from smart_vision_tool_v4.py """
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        gray = cv2.medianBlur(gray, 5)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 50, param1=100, param2=30, minRadius=10, maxRadius=50)

        results = None
        if circles is not None and len(circles[0]) >= 4:
            circles = np.round(circles[0, :]).astype("int")
            h, w = img.shape[:2]
            
            # Define 4 corners of the image frame
            img_corners = [(0, 0), (w, 0), (w, h), (0, h)] # TL, TR, BR, BL
            corner_circles = []
            temp_circles = list(circles)

            # For each image corner, find the closest circle
            for corner_x, corner_y in img_corners:
                if not temp_circles: break
                distances = [math.sqrt((c[0] - corner_x)**2 + (c[1] - corner_y)**2) for c in temp_circles]
                closest_idx = np.argmin(distances)
                corner_circles.append(temp_circles.pop(closest_idx))

            if len(corner_circles) == 4:
                # We have 4 circles, now identify and sort them
                c_tl, c_tr, c_br, c_bl = corner_circles[0], corner_circles[1], corner_circles[2], corner_circles[3]
                p_tl, p_tr, p_br, p_bl = (c_tl[0], c_tl[1]), (c_tr[0], c_tr[1]), (c_br[0], c_br[1]), (c_bl[0], c_bl[1])

                # Draw circles and lines
                for c in [c_tl, c_tr, c_br, c_bl]: cv2.circle(img, (c[0], c[1]), c[2], (0, 255, 0), 2)
                cv2.line(img, p_tl, p_tr, (255, 255, 0), 2) # A
                cv2.line(img, p_tr, p_br, (0, 255, 255), 2) # B
                cv2.line(img, p_br, p_bl, (255, 0, 0), 2)   # C
                cv2.line(img, p_bl, p_tl, (255, 0, 255), 2) # D

                # Calculate distances
                dist_a = math.hypot(p_tl[0] - p_tr[0], p_tl[1] - p_tr[1])
                dist_b = math.hypot(p_tr[0] - p_br[0], p_tr[1] - p_br[1])
                dist_c = math.hypot(p_br[0] - p_bl[0], p_br[1] - p_bl[1])
                dist_d = math.hypot(p_bl[0] - p_tl[0], p_bl[1] - p_tl[1])
                results = {"A": dist_a, "B": dist_b, "C": dist_c, "D": dist_d}
            else:
                cv2.putText(img, "Detection Failed: Could not lock 4 corners", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        else:
            cv2.putText(img, "Detection Failed: Check image quality", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        return img, results

    def update_results_display(self, _=None):
        unit = self.unit_var.get()
        if self.last_results_px:
            val_a, val_b, val_c, val_d = self.last_results_px["A"], self.last_results_px["B"], self.last_results_px["C"], self.last_results_px["D"]
            if unit == "mm":
                val_a, val_b, val_c, val_d = val_a*self.pixel_to_mm_ratio, val_b*self.pixel_to_mm_ratio, val_c*self.pixel_to_mm_ratio, val_d*self.pixel_to_mm_ratio
            elif unit == "inch":
                val_a, val_b, val_c, val_d = (val_a*self.pixel_to_mm_ratio)/25.4, (val_b*self.pixel_to_mm_ratio)/25.4, (val_c*self.pixel_to_mm_ratio)/25.4, (val_d*self.pixel_to_mm_ratio)/25.4
            self.result_text_A.configure(text=f"A 邊: {val_a:.2f} {unit}")
            self.result_text_B.configure(text=f"B 邊: {val_b:.2f} {unit}")
            self.result_text_C.configure(text=f"C 邊: {val_c:.2f} {unit}")
            self.result_text_D.configure(text=f"D 邊: {val_d:.2f} {unit}")
        else:
            self.result_text_A.configure(text=f"A 邊: -- {unit}")
            self.result_text_B.configure(text=f"B 邊: -- {unit}")
            self.result_text_C.configure(text=f"C 邊: -- {unit}")
            self.result_text_D.configure(text=f"D 邊: -- {unit}")

    def update_yolo_results_display(self):
        """Update the YOLO results display in the textbox"""
        self.yolo_results_text.delete("1.0", "end")

        if self.yolo_results is not None and len(self.yolo_results) > 0:
            for i, detection in enumerate(self.yolo_results, 1):
                text = f"{i}. {detection['class']}\n"
                text += f"   信心度: {detection['confidence']:.2%}\n"
                text += f"   位置: ({int(detection['bbox'][0])}, {int(detection['bbox'][1])})\n"
                text += "-" * 30 + "\n"
                self.yolo_results_text.insert("end", text)
        else:
            if self.show_yolo_checkbox.get():
                self.yolo_results_text.insert("1.0", "未檢測到物件")

    # --- Viewport & Config Methods ---
    def zoom(self, factor): self.zoom_level *= factor; self.process_and_display_image()
    def pan(self, x, y): self.pan_offset[0] += x; self.pan_offset[1] += y; self.process_and_display_image()
    def reset_view(self): self.zoom_level = 1.0; self.pan_offset = [0, 0]; self.process_and_display_image()

    def load_config(self):
        try:
            with open(self.config_file, 'r') as f: return json.load(f).get("pixel_to_mm_ratio", 0.1)
        except (FileNotFoundError, json.JSONDecodeError): return 0.1

    def save_config(self):
        with open(self.config_file, 'w') as f: json.dump({"pixel_to_mm_ratio": self.pixel_to_mm_ratio}, f, indent=4)

    def open_calibration_window(self):
        if not self.original_frame is None:
            CalibrationWindow(self)
        else:
            messagebox.showwarning("校準錯誤", "請先載入一張圖片以進行校準")

    def on_closing(self):
        self.stop_webcam()
        self.destroy()

class CalibrationWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("校準設定")
        self.geometry("400x300")
        self.grab_set()

        ctk.CTkLabel(self, text="校準", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        # Auto calibration from image
        auto_frame = ctk.CTkFrame(self); auto_frame.pack(pady=10, padx=10, fill="x")
        self.side_a_label = ctk.CTkLabel(auto_frame, text="讀取 A 邊像素: N/A")
        self.side_a_label.pack(pady=5)
        ctk.CTkLabel(auto_frame, text="輸入 A 邊實際長度 (mm):").pack()
        self.actual_length_entry = ctk.CTkEntry(auto_frame); self.actual_length_entry.pack(pady=5)
        ctk.CTkButton(auto_frame, text="計算並儲存比例", command=self.calculate_and_save).pack(pady=10)
        self.update_side_a_distance()

        # Manual calibration
        manual_frame = ctk.CTkFrame(self); manual_frame.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(manual_frame, text="手動輸入 mm/pixel 比例:").pack()
        self.manual_ratio_entry = ctk.CTkEntry(manual_frame, placeholder_text=f"{self.master.pixel_to_mm_ratio:.4f}")
        self.manual_ratio_entry.pack(pady=5)
        ctk.CTkButton(manual_frame, text="儲存手動比例", command=self.save_manual_ratio).pack(pady=10)

    def update_side_a_distance(self):
        if self.master.last_results_px and "A" in self.master.last_results_px:
            self.side_a_pixel_dist = self.master.last_results_px["A"]
            self.side_a_label.configure(text=f"讀取 A 邊像素: {self.side_a_pixel_dist:.2f} pixel")
        else:
            self.side_a_pixel_dist = None
            self.side_a_label.configure(text="讀取 A 邊像素: N/A (請先成功量測)")

    def calculate_and_save(self):
        if self.side_a_pixel_dist is None or self.side_a_pixel_dist == 0:
            messagebox.showerror("錯誤", "無法計算，未偵測到有效的 A 邊像素。", parent=self)
            return
        try:
            actual_length = float(self.actual_length_entry.get())
            new_ratio = actual_length / self.side_a_pixel_dist
            self.master.pixel_to_mm_ratio = new_ratio
            self.master.save_config()
            self.manual_ratio_entry.delete(0, "end"); self.manual_ratio_entry.insert(0, f"{new_ratio:.4f}")
            messagebox.showinfo("成功", f"新比例已儲存: {new_ratio:.4f}", parent=self)
            self.master.update_results_display()
            self.destroy()
        except (ValueError, TypeError):
            messagebox.showerror("錯誤", "請為實際長度輸入一個有效的數字。", parent=self)

    def save_manual_ratio(self):
        try:
            manual_ratio = float(self.manual_ratio_entry.get())
            self.master.pixel_to_mm_ratio = manual_ratio
            self.master.save_config()
            messagebox.showinfo("成功", f"手動比例已儲存: {manual_ratio}", parent=self)
            self.master.update_results_display()
            self.destroy()
        except (ValueError, TypeError):
            messagebox.showerror("錯誤", "請為比例輸入一個有效的數字。", parent=self)

if __name__ == "__main__":
    app = App()
    app.mainloop()