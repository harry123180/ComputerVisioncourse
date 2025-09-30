"""Day 5：CustomTkinter 影像檢測儀表板"""
from __future__ import annotations
from pathlib import Path

# Author: harry123180

import customtkinter as ctk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk


class InspectionApp(ctk.CTk):
    """簡化版影像檢測工具"""

    def __init__(self) -> None:
        super().__init__()
        self.title("視覺檢測儀表板 - Demo")
        self.geometry("960x600")
        ctk.set_appearance_mode("Dark")

        self.current_image_path: Path | None = None
        self.current_frame = None

        # 左側顯示區
        self.preview = ctk.CTkLabel(self, text="請載入圖片", width=640, height=480)
        self.preview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # 右側控制區
        control_frame = ctk.CTkFrame(self)
        control_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        control_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkButton(control_frame, text="載入圖片", command=self.load_image).grid(
            row=0, column=0, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(control_frame, text="轉灰階", command=self.apply_grayscale).grid(
            row=1, column=0, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(control_frame, text="高斯模糊", command=self.apply_blur).grid(
            row=2, column=0, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(control_frame, text="邊緣偵測", command=self.apply_edges).grid(
            row=3, column=0, padx=10, pady=10, sticky="ew")

        self.status = ctk.CTkLabel(control_frame, text="未載入資料", anchor="w")
        self.status.grid(row=4, column=0, padx=10, pady=(20, 10), sticky="ew")

    def load_image(self) -> None:
        """透過檔案選擇器載入圖片"""
        path = filedialog.askopenfilename(
            title="選擇影像",
            filetypes=[("Image", "*.jpg *.png *.bmp"), ("All", "*.*")],
        )
        if not path:
            return
        self.current_image_path = Path(path)
        self.update_preview(cv2.imread(path))
        self.status.configure(text=f"載入圖片：{self.current_image_path.name}")

    def apply_grayscale(self) -> None:
        """將當前影像轉為灰階顯示"""
        if self.current_frame is None:
            messagebox.showinfo("提醒", "請先載入圖片")
            return
        gray = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2GRAY)
        self.update_preview(gray)
        self.status.configure(text="已套用灰階")

    def apply_blur(self) -> None:
        if self.current_frame is None:
            messagebox.showinfo("提醒", "請先載入圖片")
            return
        blurred = cv2.GaussianBlur(self.current_frame, (9, 9), 0)
        self.update_preview(blurred)
        self.status.configure(text="已套用高斯模糊")

    def apply_edges(self) -> None:
        if self.current_frame is None:
            messagebox.showinfo("提醒", "請先載入圖片")
            return
        gray = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 80, 160)
        self.update_preview(edges)
        self.status.configure(text="已套用邊緣偵測")

    def update_preview(self, frame) -> None:
        """更新右側預覽區塊"""
        if frame is None:
            return
        self.current_frame = frame.copy()
        if frame.ndim == 2:
            display = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        else:
            display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image = Image.fromarray(display)
        image = image.resize((640, 480))
        photo = ImageTk.PhotoImage(image)
        self.preview.configure(image=photo)
        self.preview.image = photo  # 保持參考避免被 GC


def main() -> None:
    app = InspectionApp()
    app.mainloop()


if __name__ == "__main__":
    main()
