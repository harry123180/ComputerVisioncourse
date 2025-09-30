import customtkinter as ctk
from tkinter import messagebox

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("視覺辨識軟體 - 階段一")
        self.geometry("1200x700")
        ctk.set_appearance_mode("dark")

        # --- Main Layout ---
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Left Frame (Image Display) ---
        self.image_frame = ctk.CTkFrame(self)
        self.image_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.image_label = ctk.CTkLabel(self.image_frame, text="影像顯示區域")
        self.image_label.pack(expand=True, fill="both")

        # --- Right Frame (Controls) ---
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # --- Control Widgets ---
        # Each widget is linked to a placeholder callback function.

        # 1. Mode Switch
        self.mode_label = ctk.CTkLabel(self.control_frame, text="模式切換")
        self.mode_label.pack(pady=5, padx=10, anchor="w")
        self.mode_var = ctk.StringVar(value="Image")
        self.radio_image = ctk.CTkRadioButton(self.control_frame, text="靜態圖片", variable=self.mode_var, value="Image", command=self.switch_mode)
        self.radio_image.pack(pady=5, padx=20, anchor="w")
        self.radio_webcam = ctk.CTkRadioButton(self.control_frame, text="Webcam", variable=self.mode_var, value="Webcam", command=self.switch_mode)
        self.radio_webcam.pack(pady=5, padx=20, anchor="w")

        # 2. Webcam Controls
        self.webcam_label = ctk.CTkLabel(self.control_frame, text="Webcam 控制")
        self.webcam_label.pack(pady=5, padx=10, anchor="w")
        self.camera_options = ["Camera 0", "Camera 1"] # Placeholder
        self.camera_var = ctk.StringVar(value=self.camera_options[0])
        self.camera_menu = ctk.CTkOptionMenu(self.control_frame, variable=self.camera_var, values=self.camera_options, command=self.on_placeholder_click)
        self.camera_menu.pack(pady=5, padx=10, fill="x")
        self.btn_open_webcam = ctk.CTkButton(self.control_frame, text="開啟 Webcam", command=self.on_placeholder_click)
        self.btn_open_webcam.pack(pady=5, padx=10, fill="x")

        # 3. Image Controls
        self.image_control_label = ctk.CTkLabel(self.control_frame, text="圖片控制")
        self.image_control_label.pack(pady=5, padx=10, anchor="w")
        self.btn_load_image = ctk.CTkButton(self.control_frame, text="載入圖片", command=self.on_placeholder_click)
        self.btn_load_image.pack(pady=5, padx=10, fill="x")

        # 4. Processing Controls
        self.process_label = ctk.CTkLabel(self.control_frame, text="計算與設定")
        self.process_label.pack(pady=(20, 5), padx=10, anchor="w")
        self.check_show_results = ctk.CTkCheckBox(self.control_frame, text="顯示計算結果", command=self.on_placeholder_click)
        self.check_show_results.pack(pady=5, padx=10, anchor="w")
        
        self.unit_label = ctk.CTkLabel(self.control_frame, text="單位選擇")
        self.unit_label.pack(pady=5, padx=10, anchor="w")
        self.unit_var = ctk.StringVar(value="pixel")
        self.unit_menu = ctk.CTkOptionMenu(self.control_frame, variable=self.unit_var, values=["pixel", "mm", "inch"], command=self.on_placeholder_click)
        self.unit_menu.pack(pady=5, padx=10, fill="x")

        # 5. Results Display
        self.results_label = ctk.CTkLabel(self.control_frame, text="計算結果", font=ctk.CTkFont(size=16, weight="bold"))
        self.results_label.pack(pady=(20, 5), padx=10, anchor="w")
        self.results_text = ctk.CTkTextbox(self.control_frame, height=120)
        self.results_text.pack(pady=5, padx=10, fill="x")
        self.results_text.insert("0.0", "結果將顯示於此...")
        self.results_text.configure(state="disabled")

        # 6. Save Button
        self.btn_save = ctk.CTkButton(self.control_frame, text="保存結果", command=self.on_placeholder_click)
        self.btn_save.pack(pady=20, padx=10, fill="x")
        
        # --- Initial UI State ---
        self.switch_mode()

    def switch_mode(self):
        """Enable/disable controls based on the selected mode."""
        mode = self.mode_var.get()
        if mode == "Image":
            self.btn_load_image.configure(state="normal")
            self.camera_menu.configure(state="disabled")
            self.btn_open_webcam.configure(state="disabled")
        else: # Webcam mode
            self.btn_load_image.configure(state="disabled")
            self.camera_menu.configure(state="normal")
            self.btn_open_webcam.configure(state="normal")
        print(f"Switched to {mode} mode.")

    def on_placeholder_click(self, *args):
        """Placeholder callback for buttons that are not yet implemented."""
        print(f"A control was clicked. Value: {args if args else 'N/A'}")

if __name__ == "__main__":
    app = App()
    app.mainloop()