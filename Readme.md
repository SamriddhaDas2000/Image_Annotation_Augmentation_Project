# An-Augmenter: Image Annotation and Augmentation Tool

![Logo](https://img.shields.io/badge/Built%20With-Python%203.12-blue)

Welcome to **An-Augmenter**, a powerful and user-friendly **Image Annotation** and **Augmentation** tool designed to simplify dataset preparation for AI/ML projects.
This software allows you to quickly **annotate images**, **assign classes**, and **perform smart augmentations** — all through an **interactive GUI**.

---

## ✨ Features

- 🎨 Intuitive **Bounding Box Annotation** with class labeling
- 📂 Load image folders and class names easily
- 🖌️ Switch between **Select** and **Draw** modes
- 🔄 **On-the-fly Image Augmentation** (flip, rotate, blur, noise, brightness, etc.)
- 📜 Save annotations automatically in **YOLO format**
- 📺 Embedded **instruction slides** and **workflow overview**
- 🌐 Local server to watch a tutorial video (optional)
- 🖼️ Scrollable canvas for large images
- 🧠 **Augmentation settings panel** with real-time configuration
- 🛠️ Supports **Python 3.12**

---

## 📥 How to Download

```bash
git clone https://github.com/SamriddhaDas2000/Image_Annotation_Augmentation_Project.git
cd Image_Annotation_Augmentation_Project
```

---

## 📦 Installation

Make sure you have **Python 3.12** installed.

```bash
pip install -r requirements.txt
```

(Optional) You can also create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🚀 How to Run

```bash
python Image_annotater_modified_final.py
```

This will launch the GUI automatically.

---

## 🔗 Software Workflow

1. **Welcome Screen**
   - Navigate through "Welcome", "Instructions", and "Workflow Overview."
   - Option to skip directly to the annotator.

2. **Main Annotation Window**
   - Load an image folder and class text file.
   - Draw bounding boxes with class assignment.
   - Modify or delete annotations easily.

3. **Modes**
   - **Select Mode:** Choose and highlight existing annotations.
   - **Draw Mode:** Create new bounding boxes.

4. **Saving**
   - Annotations are saved automatically in YOLO format, JSON and XML format as per the user requirement beside the images.

5. **Image Augmentation**
   - Click "Augment Images" → Choose transformations like flip, rotate, noise, blur, etc.
   - Save augmented images and updated annotations.

6. **Video Tutorial Link**
   - Click on the link for software demonstration -> (https://drive.google.com/file/d/1XJNHgAtaJI-TmCalsGj5csDTL6A5jbMP/view?usp=sharing).

---

## 📂 Folder Structure

```
Image_Annotation_Augmentation_Project/
├── Image_annotater_modified_final.py         # Main GUI script
├── image_augmenter_modified.py               # Augmentation logic
├── requirements.txt                          # Required libraries
├── README.md                                 # This documentation
├── Picture3.jpg                              # Welcome background image
├── workflow.jpg                              # Workflow illustration
├── test_codes                                # codes for testing the GUI
└── (Your Image Datasets)

```

---

## 🧠 Tech Stack

- Python 3.12
- Tkinter (GUI framework)
- Pillow (Image Processing)
- OpenCV (cv2)
- Albumentations (Augmentation)
- Numpy

---

## 🛠️ Future Improvements

- Add **polygon annotations** (besides rectangles)
- Add **dataset splitting** (train/val/test split)

---

<!-- ## 📜 License

Feel free to modify, enhance, or use this project for personal, educational, or academic purposes.
(You can add a license like MIT, Apache 2.0, etc. if needed.)

--- -->
