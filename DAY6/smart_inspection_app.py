"""Day 6：整合 YOLO 與簡易量測的 GUI"""
from __future__ import annotations
from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk

# Author: harry123180

try:
    from ultralytics import YOLO
except ImportError:  # pragma: no cover
    YOLO = None


class SmartInspectionApp(ctk.CTk):
    """結合 YOLO 推論與簡易像素量測的示範"""

    def __init__(self) -> None:
        super().__init__()
        self.title("Day6 智慧檢測 Demo")
        self.geometry("1100x680")
        ctk.set_appearance_mode("System")

        self.image_panel = ctk.CTkLabel(self, text="請載入圖片", width=720, height=540)
        self.image_panel.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        control = ctk.CTkFrame(self)
        control.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        control.grid_rowconfigure(5, weight=1)

        ctk.CTkButton(control, text="載入圖片", command=self.load_image).grid(
            row=0, column=0, padx=10, pady=10, sticky="ew"
        )
        ctk.CTkButton(control, text="執行 YOLO 推論", command=self.run_inference).grid(
            row=1, column=0, padx=10, pady=10, sticky="ew"
        )

        ctk.CTkLabel(control, text="像素換算 (mm/pixel)").grid(
            row=2, column=0, padx=10, pady=(20, 5), sticky="w"
        )
        self.ratio_entry = ctk.CTkEntry(control, placeholder_text="0.10")
        self.ratio_entry.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        ctk.CTkButton(control, text="計算寬度", command=self.calculate_width).grid(
            row=4, column=0, padx=10, pady=10, sticky="ew"
        )

        self.text_box = ctk.CTkTextbox(control, width=320)
        self.text_box.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")
        self.text_box.insert("1.0", "尚未載入圖片\n")
        self.text_box.configure(state="disabled")

        self.current_image_path: Path | None = None
        self.current_bgr = None
        self.last_detections = []

        self.yolo_model = self._load_model()

    def _load_model(self):
        """嘗試載入 YOLO 權重"""
        if YOLO is None:
            messagebox.showwarning("提示", "未安裝 ultralytics，YOLO 相關功能將停用")
            return None

        model_path = Path(__file__).resolve().parent.parent / "DAY3" / "runs" / "demo_yolo11" / "weights" / "best.pt"
        if not model_path.exists():
            model_path = Path(__file__).resolve().parent.parent / "DAY3" / "models" / "yolo11n.pt"
        if not model_path.exists():
            messagebox.showinfo("提醒", "找不到 YOLO 權重，請先完成 Day3 的訓練或下載")
            return None

        return YOLO(str(model_path))

    def load_image(self) -> None:
        """選擇圖片並顯示於主視窗"""
        file_path = filedialog.askopenfilename(
            title="選擇圖片",
            filetypes=[("Image", "*.jpg *.png *.bmp"), ("All Files", "*.*")],
        )
        if not file_path:
            return

        self.current_image_path = Path(file_path)
        self.current_bgr = cv2.imread(file_path)
        if self.current_bgr is None:
            messagebox.showerror("錯誤", "無法讀取圖片")
            return

        self.last_detections = []
        self._show_on_panel(self.current_bgr)
        self._log(f"載入圖片：{self.current_image_path.name}")

    def run_inference(self) -> None:
        """執行 YOLO 推論並繪製框線"""
        if self.current_bgr is None:
            messagebox.showinfo("提醒", "請先載入圖片")
            return
        if self.yolo_model is None:
            messagebox.showinfo("提醒", "尚未載入 YOLO 模型")
            return

        results = self.yolo_model.predict(source=self.current_bgr, verbose=False)
        annotated = self.current_bgr.copy()
        detections = []

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                confidence = float(box.conf[0])
                cls_id = int(box.cls[0])
                label = self.yolo_model.names.get(cls_id, str(cls_id))
                detections.append((x1, y1, x2, y2, label, confidence))

                cv2.rectangle(annotated, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                caption = f"{label} {confidence:.2f}"
                cv2.putText(annotated, caption, (int(x1), int(y1) - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        self.last_detections = detections
        self._show_on_panel(annotated)

        if detections:
            self._log(f"偵測到 {len(detections)} 個物件")
        else:
            self._log("未偵測到任何物件")

    def calculate_width(self) -> None:
        """根據框線估算寬度"""
        if not self.last_detections:
            messagebox.showinfo("提醒", "請先執行 YOLO 推論")
            return

        try:
            ratio = float(self.ratio_entry.get() or 0.10)
        except ValueError:
            messagebox.showerror("錯誤", "請輸入正確的數值 (mm/pixel)")
            return

        logs = []
        for index, (x1, _, x2, _, label, _) in enumerate(self.last_detections, start=1):
            pixel_width = abs(x2 - x1)
            mm_width = pixel_width * ratio
            logs.append(f"#{index} {label}: {pixel_width:.1f} px ≈ {mm_width:.2f} mm")

        self._log("\n".join(logs))

    def _show_on_panel(self, bgr_image) -> None:
        """將 BGR 影像顯示在 GUI 上"""
        rgb = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb).resize((720, 540))
        photo = ImageTk.PhotoImage(image)
        self.image_panel.configure(image=photo)
        self.image_panel.image = photo

    def _log(self, text: str) -> None:
        self.text_box.configure(state="normal")
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", text + "\n")
        self.text_box.configure(state="disabled")


def main() -> None:
    app = SmartInspectionApp()
    app.mainloop()


if __name__ == "__main__":
    main()
