import sys
import os
import cv2
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QLabel, QVBoxLayout, QWidget, QPushButton, QMenuBar, QAction, QHBoxLayout, QComboBox, QListWidget, QScrollArea, QInputDialog
)
from PyQt5.QtGui import QImage, QPixmap, QColor, QPainter, QCursor
from PyQt5.QtCore import Qt, QPoint


class AnnotationTool(QMainWindow):
    def __init__(self, image_dir=None, class_file=None):
        super().__init__()
        self.image_dir = image_dir
        self.class_file = class_file
        self.image_paths = []
        self.current_image_index = 0
        self.classes = []
        self.save_dir = None
        self.zoom_factor = 1.0
        self.drawing = False  # To track if drawing is in progress
        self.rect_start = QPoint()  # Start point of the rectangle
        self.rect_end = QPoint()  # End point of the rectangle
        self.bounding_boxes = []  # List to store bounding boxes
        self.current_class = ""  # Current class for the bounding box
        self.image_width = 0  # Width of the current image
        self.image_height = 0  # Height of the current image
        self.colors = {}  # Dictionary to store colors for each class
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Simplified Annotation Tool")
        self.setGeometry(100, 100, 1200, 800)

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        # Left Panel for Buttons
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout(self.left_panel)
        self.main_layout.addWidget(self.left_panel, stretch=1)

        # Buttons
        self.btn_open = QPushButton("Open Image", self)
        self.btn_open.clicked.connect(self.open_image)
        self.left_layout.addWidget(self.btn_open)

        self.btn_open_dir = QPushButton("Open Directory", self)
        self.btn_open_dir.clicked.connect(self.open_directory)
        self.left_layout.addWidget(self.btn_open_dir)

        self.btn_change_save_dir = QPushButton("Change Save Dir", self)
        self.btn_change_save_dir.clicked.connect(self.change_save_dir)
        self.left_layout.addWidget(self.btn_change_save_dir)

        self.btn_next = QPushButton("Next Image", self)
        self.btn_next.clicked.connect(self.next_image)
        self.left_layout.addWidget(self.btn_next)

        self.btn_prev = QPushButton("Previous Image", self)
        self.btn_prev.clicked.connect(self.previous_image)
        self.left_layout.addWidget(self.btn_prev)

        self.btn_save = QPushButton("Save", self)
        self.btn_save.clicked.connect(self.save_file)
        self.left_layout.addWidget(self.btn_save)

        self.btn_create_rect = QPushButton("Create RectBox", self)
        self.btn_create_rect.clicked.connect(self.create_rect_box)
        self.left_layout.addWidget(self.btn_create_rect)

        # Image Label
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.image_label, stretch=4)

        # Right Panel for Class Labels and Image List
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout(self.right_panel)
        self.main_layout.addWidget(self.right_panel, stretch=1)

        # Class Labels Dropdown
        self.class_combo = QComboBox(self)
        self.right_layout.addWidget(self.class_combo)

        # Image List
        self.image_list = QListWidget(self)
        self.image_list.itemClicked.connect(self.load_selected_image)
        self.right_layout.addWidget(self.image_list)

        # Load classes if class file is provided
        if self.class_file and os.path.exists(self.class_file):
            with open(self.class_file, "r") as f:
                self.classes = [line.strip() for line in f.readlines()]
                self.class_combo.addItems(self.classes)
                # Assign colors to each class
                for i, class_name in enumerate(self.classes):
                    self.colors[class_name] = QColor(255 // (i + 1), 100, 100)

        # Load images if image folder is provided
        if self.image_dir and os.path.exists(self.image_dir):
            self.load_images_from_directory(self.image_dir)

        # Menu Bar
        self.create_menu_bar()

    def load_images_from_directory(self, dir_path):
        """Load images from the specified directory and update the UI."""
        self.image_paths = [
            os.path.join(dir_path, f)
            for f in os.listdir(dir_path)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))
        ]
        if self.image_paths:
            self.current_image_index = 0
            self.load_image(self.image_paths[self.current_image_index])
            self.image_list.clear()
            for img_path in self.image_paths:
                self.image_list.addItem(os.path.basename(img_path))

    def create_menu_bar(self):
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("File")
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_image)
        file_menu.addAction(open_action)

        open_dir_action = QAction("Open Directory", self)
        open_dir_action.triggered.connect(self.open_directory)
        file_menu.addAction(open_dir_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save As", self)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)

        change_save_dir_action = QAction("Change Save Dir", self)
        change_save_dir_action.triggered.connect(self.change_save_dir)
        file_menu.addAction(change_save_dir_action)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # Edit Menu
        edit_menu = menubar.addMenu("Edit")
        create_rect_action = QAction("Create RectBox", self)
        create_rect_action.triggered.connect(self.create_rect_box)
        edit_menu.addAction(create_rect_action)

        edit_label_action = QAction("Edit Label", self)
        edit_label_action.triggered.connect(self.edit_label)
        edit_menu.addAction(edit_label_action)

        delete_rect_action = QAction("Delete RectBox", self)
        delete_rect_action.triggered.connect(self.delete_rect_box)
        edit_menu.addAction(delete_rect_action)

        draw_square_action = QAction("Draw Square", self)
        draw_square_action.triggered.connect(self.draw_square)
        edit_menu.addAction(draw_square_action)

        # View Menu
        view_menu = menubar.addMenu("View")
        auto_save_action = QAction("Auto Save Mode", self)
        auto_save_action.setCheckable(True)
        view_menu.addAction(auto_save_action)

        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out_action)

        fit_window_action = QAction("Fit Window", self)
        fit_window_action.triggered.connect(self.fit_window)
        view_menu.addAction(fit_window_action)

    def open_image(self):
        options = QFileDialog.Options()
        image_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)
        if image_path:
            self.image_paths = [image_path]
            self.current_image_index = 0
            self.load_image(image_path)

    def open_directory(self):
        options = QFileDialog.Options()
        dir_path = QFileDialog.getExistingDirectory(self, "Open Directory", options=options)
        if dir_path:
            self.image_dir = dir_path
            self.load_images_from_directory(dir_path)

    def change_save_dir(self):
        options = QFileDialog.Options()
        self.save_dir = QFileDialog.getExistingDirectory(self, "Change Save Directory", options=options)

    def load_image(self, image_path):
        self.image = cv2.imread(image_path)
        if self.image is None:
            print(f"Error: Unable to load image at {image_path}")
            return
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.image_width = self.image.shape[1]
        self.image_height = self.image.shape[0]
        self.bounding_boxes = []  # Clear bounding boxes for the new image
        self.update_image_display()

    def update_image_display(self):
        """Draw the image and any bounding boxes."""
        h, w, ch = self.image.shape
        bytes_per_line = ch * w
        q_img = QImage(self.image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)

        # Draw all saved bounding boxes
        painter = QPainter(pixmap)
        for box in self.bounding_boxes:
            color = self.colors.get(box["class"], QColor(255, 0, 0))  # Default to red if class color not found
            painter.setPen(color)
            x1 = int((box["center_x"] - box["width"] / 2) * self.image_width)
            y1 = int((box["center_y"] - box["height"] / 2) * self.image_height)
            x2 = int((box["center_x"] + box["width"] / 2) * self.image_width)
            y2 = int((box["center_y"] + box["height"] / 2) * self.image_height)
            painter.drawRect(x1, y1, x2 - x1, y2 - y1)
        painter.end()

        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def create_rect_box(self):
        """Enable drawing mode and change cursor to crosshair."""
        self.drawing = True
        self.setCursor(Qt.CrossCursor)
        print("Drawing mode enabled. Click and drag to draw a rectangle.")

    def mousePressEvent(self, event):
        """Capture the start point of the rectangle."""
        if self.drawing and event.button() == Qt.LeftButton:
            self.rect_start = event.pos()
            self.rect_end = event.pos()

    def mouseMoveEvent(self, event):
        """Update the end point of the rectangle while dragging."""
        if self.drawing:
            self.rect_end = event.pos()
            self.update_image_display()

    def mouseReleaseEvent(self, event):
        """Finalize the rectangle and assign a class."""
        if self.drawing and event.button() == Qt.LeftButton:
            self.rect_end = event.pos()
            self.drawing = False
            self.setCursor(Qt.ArrowCursor)  # Reset cursor

            # Get the class from the dropdown or create a new class
            if self.class_combo.count() > 0:
                self.current_class = self.class_combo.currentText()
            else:
                # If no class file is provided, create a new class
                class_name, ok = QInputDialog.getText(self, "New Class", "Enter class name:")
                if ok and class_name:
                    self.classes.append(class_name)
                    self.class_combo.addItem(class_name)
                    self.current_class = class_name
                    # Save the new class to the class file
                    if self.class_file:
                        with open(self.class_file, "a") as f:
                            f.write(f"{class_name}\n")

            if self.current_class:
                # Normalize coordinates and store the bounding box
                self.save_bounding_box()
            else:
                print("No class selected. Bounding box not saved.")

    def save_bounding_box(self):
        """Save the bounding box in YOLO format."""
        # Normalize coordinates
        x1 = min(self.rect_start.x(), self.rect_end.x())
        y1 = min(self.rect_start.y(), self.rect_end.y())
        x2 = max(self.rect_start.x(), self.rect_end.x())
        y2 = max(self.rect_start.y(), self.rect_end.y())

        # Calculate center, width, and height as fractions
        center_x = ((x1 + x2) / 2) / self.image_width
        center_y = ((y1 + y2) / 2) / self.image_height
        width = (x2 - x1) / self.image_width
        height = (y2 - y1) / self.image_height

        # Store the bounding box
        self.bounding_boxes.append({
            "class": self.current_class,
            "center_x": center_x,
            "center_y": center_y,
            "width": width,
            "height": height
        })

        print(f"Bounding box saved for class: {self.current_class}")
        self.update_image_display()

    def save_file(self):
        """Save bounding boxes in YOLO format."""
        if self.save_dir and self.image_paths:
            image_name = os.path.basename(self.image_paths[self.current_image_index])
            label_name = os.path.splitext(image_name)[0] + ".txt"
            label_path = os.path.join(self.save_dir, label_name)

            with open(label_path, "w") as f:
                for box in self.bounding_boxes:
                    class_index = self.classes.index(box["class"])
                    f.write(f"{class_index} {box['center_x']} {box['center_y']} {box['width']} {box['height']}\n")

            print(f"Labels saved to {label_path}")

    def save_file_as(self):
        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)
        if save_path:
            cv2.imwrite(save_path, cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR))
            print(f"Saved to {save_path}")

    def next_image(self):
        """Move to the next image and auto-save the current annotations."""
        if self.image_paths and self.current_image_index < len(self.image_paths) - 1:
            self.save_file()  # Auto-save before moving to the next image
            self.current_image_index += 1
            self.load_image(self.image_paths[self.current_image_index])

    def previous_image(self):
        """Move to the previous image and auto-save the current annotations."""
        if self.image_paths and self.current_image_index > 0:
            self.save_file()  # Auto-save before moving to the previous image
            self.current_image_index -= 1
            self.load_image(self.image_paths[self.current_image_index])

    def edit_label(self):
        print("Edit Label")

    def delete_rect_box(self):
        print("Delete RectBox")

    def draw_square(self):
        print("Draw Square")

    def zoom_in(self):
        self.zoom_factor *= 1.1
        self.update_image_display()

    def zoom_out(self):
        self.zoom_factor /= 1.1
        self.update_image_display()

    def fit_window(self):
        self.zoom_factor = 1.0
        self.update_image_display()

    def load_selected_image(self, item):
        selected_image = os.path.join(self.image_dir, item.text())
        self.load_image(selected_image)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Simplified Annotation Tool")
    parser.add_argument("--image_dir", type=str, help="Path to the folder containing images")
    parser.add_argument("--class_file", type=str, help="Path to the text file containing class names")
    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = AnnotationTool(image_dir=args.image_dir, class_file=args.class_file)
    window.show()
    sys.exit(app.exec_())