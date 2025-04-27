import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import os

class BBoxLabelingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bounding Box Labeling Tool")

        self.canvas = tk.Canvas(root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.btn_load = tk.Button(root, text="Load Image", command=self.load_image)
        self.btn_load.pack()

        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

        self.image = None
        self.tk_image = None
        self.rect = None
        self.start_x = self.start_y = 0
        self.scale_factor = 1.0
        self.image_path = ""
        self.annotations = []

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
        if not file_path:
            return

        self.image_path = file_path
        self.image = Image.open(file_path)

        # Apply EXIF transpose to correct orientation
        self.image = ImageOps.exif_transpose(self.image)

        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        img_width, img_height = self.image.size
        self.scale_factor = min(canvas_width / img_width, canvas_height / img_height)
        new_width = int(img_width * self.scale_factor)
        new_height = int(img_height * self.scale_factor)

        resized_image = self.image.resize((new_width, new_height), Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def on_mouse_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)

    def on_mouse_drag(self, event):
        if self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_mouse_release(self, event):
        end_x, end_y = event.x, event.y
        img_width, img_height = self.image.size

        x1, y1 = min(self.start_x, end_x) / self.scale_factor, min(self.start_y, end_y) / self.scale_factor
        x2, y2 = max(self.start_x, end_x) / self.scale_factor, max(self.start_y, end_y) / self.scale_factor

        x_center = (x1 + x2) / (2 * img_width)
        y_center = (y1 + y2) / (2 * img_height)
        width = (x2 - x1) / img_width
        height = (y2 - y1) / img_height

        self.annotations.append(f"0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

        self.save_annotations()

    def save_annotations(self):
        label_path = os.path.splitext(self.image_path)[0] + ".txt"
        with open(label_path, "w") as f:
            f.write("\n".join(self.annotations))
        messagebox.showinfo("Saved", f"Annotations saved to {label_path}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = BBoxLabelingApp(root)
    root.mainloop()
