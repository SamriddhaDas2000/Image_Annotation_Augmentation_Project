import cv2
import torch
import threading
import tkinter as tk
from PIL import Image, ImageTk
from ultralytics import YOLO

# Check if CUDA is available
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the trained YOLO model for person detection
model_person = YOLO("yolo11n.pt").to(device)  # Load YOLO model for person detection

detection_active = False
cap = cv2.VideoCapture(0)

def start_detection():
    global detection_active
    detection_active = True
    process_video()

def stop_detection():
    global detection_active
    detection_active = False

def quit_app():
    global cap
    detection_active = False
    cap.release()
    cv2.destroyAllWindows()
    root.quit()

def process_video():
    global detection_active, cap
    if not detection_active:
        return

    ret, frame = cap.read()
    if ret:
        results_person = model_person(frame, conf=0.75, device=device)

        # Process person detection
        for result in results_person:
            for det in result.boxes:
                class_id = int(det.cls[0])
                if class_id == 0:  # COCO dataset class ID for person is 0
                    x1, y1, x2, y2 = map(int, det.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blue box for person
                    confidence_score = f"{det.conf[0]:.2f}"
                    label = f"Person: {confidence_score}"
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Convert frame for tkinter
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(image=img)
        video_label.img_tk = img_tk
        video_label.config(image=img_tk)

    if detection_active:
        root.after(10, process_video)

# GUI Setup
root = tk.Tk()
root.title("Person Detection GUI")
root.geometry("800x480")

# Styling
root.configure(bg="black")  # Set background color

frame_controls = tk.Frame(root, bg="navy")  # Left panel with navy blue background
frame_controls.pack(side=tk.LEFT, fill=tk.Y)

btn_style = {"font": ("Arial", 12, "bold"), "fg": "white", "bg": "#1E90FF", "width": 15, "height": 2}

btn_start = tk.Button(frame_controls, text="Start Detection", command=start_detection, **btn_style)
btn_start.pack()

btn_stop = tk.Button(frame_controls, text="Stop Detection", command=stop_detection, **btn_style)
btn_stop.pack(pady=10)

btn_quit = tk.Button(frame_controls, text="Quit", command=quit_app, **btn_style)
btn_quit.pack()

video_label = tk.Label(root, bg="black")  # Initially black screen for video feed
video_label.pack(expand=True, fill=tk.BOTH)

root.mainloop()
