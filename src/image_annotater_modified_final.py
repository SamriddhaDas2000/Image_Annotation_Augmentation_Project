import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk, ImageDraw, ImageOps
import colorsys
from collections import defaultdict
from image_augmenter_modified import ImageAugmenter
import webbrowser
import http.server
import socketserver
import threading
import functools
import json
import xml.etree.ElementTree as ET

class WelcomeScreen:


    print(os.getcwd())
    def __init__(self, root, on_finish_callback):
        self.root = root
        self.root.title("An-Augmenter")
        self.on_finish = on_finish_callback
        self.slide = 0
        self.slides = [self.show_logo_screen, self.show_instruction_screen, self.show_workflow_screen]
        self.frame = tk.Frame(self.root, bg='lightblue')
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.show_logo_screen()


    def add_footer(self, parent_frame):
        footer = tk.Frame(parent_frame, bg='lightblue')
        footer.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        tk.Label(footer, text="Version 1.0.0", bg='lightblue', font=("Helvetica", 8, "bold")).pack()
        tk.Label(footer, text="Created by: Samriddha Das", bg='lightblue', font=("Helvetica", 8, "bold")).pack()
        tk.Label(footer, text="samriddha.das@ndsu.edu", bg='lightblue', font=("Helvetica", 8, "bold")).pack()

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def show_logo_screen(self):
        self.clear_frame()

        # Top navy blue header
        header = tk.Frame(self.frame, bg='lightblue', height=80)
        header.pack(fill=tk.X)

        welcome_label = tk.Label(header, text="!! WELCOME !!", font=("Helvetica", 30, "bold"), bg='lightblue', fg='black')
        welcome_label.pack(pady=1)

        # Main area with canvas
        self.main_area = tk.Canvas(self.frame, highlightthickness=0, bg = 'black')
        self.main_area.pack(fill=tk.BOTH, expand=True)

        self.original_bg_image = Image.open("docs\logo.JPG")

        self.skip_button = tk.Button(self.main_area, text="Skip", command=self.on_finish, bg="lightgray", width=12, height=2, font=("Helvetica", 16, "bold"))
        self.next_button = tk.Button(self.main_area, text="Next", command=self.next_slide, bg="lightblue", width=12, height=2, font=("Helvetica", 16, "bold"))

        self.add_footer(self.frame)

        self.main_area.bind("<Configure>", self.resize_background)



    # def resize_background(self, event):
    #     canvas_width = event.width
    #     canvas_height = event.height

    #     resized_bg = self.original_bg_image.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
    #     self.bg_photo = ImageTk.PhotoImage(resized_bg)

    #     self.main_area.delete("all")
    #     self.main_area.create_image(0, 0, image=self.bg_photo, anchor='nw')

    #     # Display instruction text in center top
    #     instruction_text = "👉 To learn about the software and instructions, press Next.\n👉 Or press Skip to dive straight into annotating!"
    #     self.main_area.create_text(canvas_width // 2, 90, text=instruction_text, font=("Helvetica", 18, "bold"), fill="white", justify="left")

    #     # Create arrows
    #     # Arrow to Skip (bottom-left)
    #     # self.main_area.create_line(150, canvas_height - 120, 100, canvas_height - 80, arrow=tk.LAST, width=3, fill="yellow")
    #     # self.main_area.create_text(170, canvas_height - 140, text="Skip →", font=("Helvetica", 14, "bold"), fill="yellow")

    #     # # Arrow to Next (bottom-right)
    #     # self.main_area.create_line(canvas_width - 150, canvas_height - 120, canvas_width - 100, canvas_height - 80, arrow=tk.LAST, width=3, fill="yellow")
    #     # self.main_area.create_text(canvas_width - 170, canvas_height - 140, text="← Next", font=("Helvetica", 14, "bold"), fill="yellow")

    #     # Place buttons
    #     self.main_area.create_window(100, canvas_height - 40, window=self.skip_button)
    #     self.main_area.create_window(canvas_width - 100, canvas_height - 40, window=self.next_button)

    def resize_background(self, event):
        canvas_width = event.width
        canvas_height = event.height

        self.main_area.delete("all")  # Clear previous drawings

        # Get original image size
        img_width, img_height = self.original_bg_image.size

        # Calculate scale to fit image within canvas while maintaining aspect ratio
        scale = min(canvas_width / img_width, canvas_height / img_height)

        # Only resize if the image is larger than the canvas
        if scale < 1.0:
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            resized_image = self.original_bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        else:
            resized_image = self.original_bg_image.copy()
            new_width, new_height = img_width, img_height

        self.bg_photo = ImageTk.PhotoImage(resized_image)

        # Center image
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2
        self.main_area.create_image(x, y, image=self.bg_photo, anchor='nw')

        # Instruction text (stay on top, center-top)
        instruction_text = (
            "👉 To learn about the software and instructions, press Next.\n\n"

            "👉 Or press Skip to dive straight into annotating!"
        )
        self.main_area.create_text(canvas_width // 2, 70, text=instruction_text,
                                font=("Helvetica", 14, "bold"), fill="white", justify="left")

        # Place buttons
        self.main_area.create_window(100, canvas_height - 40, window=self.skip_button)
        self.main_area.create_window(canvas_width - 100, canvas_height - 40, window=self.next_button)



    def show_instruction_screen(self):
        self.clear_frame()

        # Top navy blue header
        header = tk.Frame(self.frame, bg='lightblue', height=80)
        header.pack(fill=tk.X)

        about_label = tk.Label(header, text="ℹ️ About", font=("Helvetica", 30, "bold"),bg='lightblue', fg='black')
        about_label.pack(pady=20)

        # Main area with canvas
        self.main_area = tk.Canvas(self.frame, highlightthickness=0, bg='lightgray')
        self.main_area.pack(fill=tk.BOTH, expand=True)

        self.skip_button = tk.Button(self.main_area, text="Back", command=self.prev_slide, bg="lightblue", width=12, height=2, font=("Helvetica", 16, "bold"))
        self.next_button = tk.Button(self.main_area, text="Next", command=self.next_slide, bg="lightblue", width=12, height=2, font=("Helvetica", 16, "bold"))

        self.add_footer(self.frame)

        self.main_area.bind("<Configure>", self.resize_instruction_screen)

    def resize_instruction_screen(self, event):
        canvas_width = event.width
        canvas_height = event.height

        self.main_area.delete("all")

        # About section
        about_text = (
            "An-Augmenter is a user-friendly software designed to simplify image annotation\n"
            "and augmentation for AI/ML projects. It allows quick, intuitive drawing,\n"
            "class labeling, and instant augmentation for better dataset preparation."
        )
        self.main_area.create_text(
            canvas_width // 2, 100,
            text=about_text,
            font=("Helvetica", 16),
            fill="black",
            justify="left"
        )

        # Instructions title
        self.main_area.create_text(
            canvas_width // 2, 250,
            text="📝 Instructions:",
            font=("Helvetica", 20, "bold"),
            fill="black"
        )

        # Placeholder for instruction points (you can fill them later)
        instruction_placeholder = (
            "1. Load image directory and class names prior to the start of annotating.\n"
            "2. Select mode gives the provision to choose the class you want to label.\n"
            "3. Switch to Draw Mode in order to start annotating.\n"
            "4. Annotations get saved at the same time as the bounding box creation in the same directory.\n"
            "5. Annotations can be deleted using delete bounding box feature given in the GUI.\n"
            "6. Augment images with rotation, flipping, etc. by clicking on the augment button.\n"
            "7. In order to save the augmented images location can be provided separately.\n"
            "8. Click 'Next' for a better understanding of the software with the workflow, otherwise press 'Back' \n"
            "    to go back to the main window."
        )
        self.main_area.create_text(
            canvas_width // 2, 400,
            text=instruction_placeholder,
            font=("Helvetica", 16),
            fill="black",
            justify="left"
        )

        # Place Back and Next buttons
        self.main_area.create_window(100, canvas_height - 40, window=self.skip_button)
        self.main_area.create_window(canvas_width - 100, canvas_height - 40, window=self.next_button)


    def show_workflow_screen(self):
        self.clear_frame()

        # Top header
        header = tk.Frame(self.frame, bg='lightblue', height=80)
        header.pack(fill=tk.X)

        title_label = tk.Label(header, text="🔄 Workflow Overview", font=("Helvetica", 30, "bold"), bg='lightblue', fg='black')
        title_label.pack(pady=20)

        # Main content area (canvas to allow absolute placement)
        self.content_area = tk.Canvas(self.frame, bg='white', highlightthickness=0)
        self.content_area.pack(fill=tk.BOTH, expand=True)

        # Load workflow image
        self.original_workflow_image = Image.open("docs\workflow.png")  # Replace with your real image
        self.workflow_img_label = tk.Label(self.content_area, bg='white')
        self.image_window = self.content_area.create_window(0, 0, window=self.workflow_img_label, anchor="n")

        # Link label
        self.video_link = tk.Label(
            self.content_area, text="Click here to watch the tutorial video",
            font=("Helvetica", 16, "underline"), fg="blue", cursor="hand2", bg='white'
        )
        self.link_window = self.content_area.create_window(0, 0, window=self.video_link, anchor="n")

        self.video_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://drive.google.com/file/d/1XJNHgAtaJI-TmCalsGj5csDTL6A5jbMP/view?usp=sharing"))
        self.video_link.bind("<Enter>", lambda e: self.video_link.config(fg="darkblue"))
        self.video_link.bind("<Leave>", lambda e: self.video_link.config(fg="blue"))

        # Buttons
        self.back_button = tk.Button(self.content_area, text="Back", command=self.prev_slide, bg="lightblue",
                                    width=12, height=2, font=("Helvetica", 16, "bold"))
        self.start_button = tk.Button(self.content_area, text="Start Annotating", command=self.on_finish, bg="lightgreen",
                                    width=16, height=2, font=("Helvetica", 16, "bold"))

        # Placeholders for button windows
        self.back_button_window = self.content_area.create_window(0, 0, window=self.back_button)
        self.start_button_window = self.content_area.create_window(0, 0, window=self.start_button)
        self.add_footer(self.frame)

        # Bind resize to adjust all positions
        self.content_area.bind("<Configure>", self.resize_workflow_image)


    def resize_workflow_image(self, event):
        canvas_width = event.width
        canvas_height = event.height

        max_width = canvas_width - 200  # Margin
        max_height = 550                # Max height for image

        img_ratio = self.original_workflow_image.width / self.original_workflow_image.height
        if max_width / img_ratio <= max_height:
            resized_width = max_width
            resized_height = int(max_width / img_ratio)
        else:
            resized_height = max_height
            resized_width = int(max_height * img_ratio)

        resized_img = self.original_workflow_image.resize((resized_width, resized_height))
        self.workflow_tk_img = ImageTk.PhotoImage(resized_img)
        self.workflow_img_label.config(image=self.workflow_tk_img)
        self.workflow_img_label.image = self.workflow_tk_img  # Keep reference

        # Reposition the image in canvas
        self.content_area.coords(self.image_window, canvas_width // 2, 10)

        # Reposition the link below image
        self.content_area.coords(self.link_window, canvas_width // 2, 60 + resized_height)

        # Reposition Back and Start buttons near bottom
        self.content_area.coords(self.back_button_window, 100, canvas_height - 40)
        self.content_area.coords(self.start_button_window, canvas_width - 150, canvas_height - 40)






    def add_nav_buttons(self, finish=False):
        nav = tk.Frame(self.frame, bg='white')
        nav.pack(pady=20)
        tk.Button(nav, text="Back", command=self.prev_slide, bg="lightgray").pack(side=tk.LEFT, padx=10)
        if finish:
            tk.Button(nav, text="Start Annotating", command=self.on_finish, bg="lightgreen").pack(side=tk.LEFT, padx=10)
        else:
            tk.Button(nav, text="Next", command=self.next_slide, bg="lightblue").pack(side=tk.LEFT, padx=10)

    def next_slide(self):
        self.slide += 1
        if self.slide < len(self.slides):
            self.slides[self.slide]()
        else:
            self.on_finish()

    def prev_slide(self):
        if self.slide > 0:
            self.slide -= 1
            self.slides[self.slide]()

class ImageAnnotator:
    def __init__(self, root):
        self.root = root
        self.root.title("An-Augmenter")
        self.root.configure(bg='navy')

        # Initialize variables
        self.image_folder = ""
        self.class_file = ""
        self.classes = []
        self.colors = []
        self.current_image_index = 0
        self.images = []
        self.annotations = defaultdict(list)
        self.drawing = False
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.current_class = None
        self.scale_factor = 1.0
        self.original_image = None
        self.current_bbox_ids = []
        self.mode = "select"
        self.guidelines = []
        self.selected_annotation_index = None
        self.x_offset = 0
        self.y_offset = 0
        self.augmenter = ImageAugmenter()
        self.annotation_formats = {"yolo": True, "json": False, "xml": False}
        self.stop_augmentation = False
        self.pan_start_x = None
        self.pan_start_y = None
        self.zoom_level = 1.0
        self.min_scale_factor = 1.0  # to be updated on image fit
        self.pending_box = None


        # Setup GUI
        self.setup_ui()

        # Ask for paths if not provided
        self.ask_for_paths()

    def setup_ui(self):
        # Left panel for controls
        left_panel = tk.Frame(self.root, bg='navy', width=200)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)

        # Folder and class file buttons
        tk.Button(left_panel, text="Open Image Folder", command=self.open_image_folder,
                 bg='lightblue', fg='navy').pack(pady=5, fill=tk.X)
        tk.Button(left_panel, text="Open Class File", command=self.open_class_file,
                 bg='lightblue', fg='navy').pack(pady=5, fill=tk.X)

        # Navigation buttons
        nav_frame = tk.Frame(left_panel, bg='navy')
        nav_frame.pack(pady=10, fill=tk.X)

        nav_frame.columnconfigure(0, weight=1)
        nav_frame.columnconfigure(1, weight=1)

        tk.Button(nav_frame, text="Previous", command=self.prev_image,
                bg='lightblue', fg='navy').grid(row=0, column=0, sticky="ew")

        tk.Button(nav_frame, text="Next", command=self.next_image,
                bg='lightblue', fg='navy').grid(row=0, column=1, sticky="ew")
        # Mode selection
        mode_frame = tk.Frame(left_panel, bg='navy')
        mode_frame.pack(pady=10)
        self.mode_var = tk.StringVar(value="select")
        tk.Radiobutton(mode_frame, text="Select Mode", variable=self.mode_var,
                      value="select", command=self.set_select_mode, bg='navy', fg='white',
                      selectcolor='navy', activebackground='navy').pack(anchor=tk.W)
        tk.Radiobutton(mode_frame, text="Draw Mode", variable=self.mode_var,
                      value="draw", command=self.set_draw_mode, bg='navy', fg='white',
                      selectcolor='navy', activebackground='navy').pack(anchor=tk.W)

        # Class selection
        self.class_var = tk.StringVar()
        self.class_dropdown = tk.OptionMenu(left_panel, self.class_var, "")
        self.class_dropdown.pack(pady=10, fill=tk.X)
        self.class_var.set("Select Class")

        # Draw button
        tk.Button(left_panel, text="Draw Bounding Box", command=self.set_draw_mode,
                 bg='lightblue', fg='navy').pack(pady=5, fill=tk.X)

        # Delete button
        tk.Button(left_panel, text="Delete Selected", command=self.delete_selected,
                 bg='lightblue', fg='navy').pack(pady=5, fill=tk.X)

        tk.Label(left_panel, text="Save Format:", bg='navy', fg='white').pack(pady=(10, 0))
        self.format_vars = {
            "yolo": tk.BooleanVar(value=True),
            "json": tk.BooleanVar(value=False),
            "xml": tk.BooleanVar(value=False)
                }
        for fmt in ["yolo", "json", "xml"]:
            tk.Checkbutton(left_panel, text=fmt.upper(), variable=self.format_vars[fmt],
                        bg='navy', fg='white', selectcolor='navy',
                        command=self.update_annotation_format).pack(anchor=tk.W)


        # Annotations list
        tk.Label(left_panel, text="Annotations:", bg='navy', fg='white').pack(pady=5)
        self.annotations_list = tk.Listbox(left_panel, height=10)
        self.annotations_list.pack(fill=tk.BOTH, expand=True)
        self.annotations_list.bind('<<ListboxSelect>>', self.on_annotation_select)

        tk.Button(left_panel, text="Augment Images", command=self.setup_augmentation_ui,
          bg='lightblue', fg='navy').pack(pady=5, fill=tk.X)

        # Image display with scrollbars
        self.image_frame = tk.Frame(self.root, bg='gray')
        self.image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.image_frame, bg='gray', cursor="crosshair")
        self.h_scroll = tk.Scrollbar(self.image_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.v_scroll = tk.Scrollbar(self.image_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)
        self.canvas = tk.Canvas(self.image_frame, bg='gray', cursor="fleur")


        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Bind mouse events
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)  # Windows
        self.canvas.bind("<Button-4>", self.on_mousewheel)    # Linux scroll up
        self.canvas.bind("<Button-5>", self.on_mousewheel)    # Linux scroll down
        self.canvas.bind("<ButtonPress-2>", self.on_middle_click)
        self.canvas.bind("<B2-Motion>", self.on_middle_drag)
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        self.canvas.bind("<Motion>", self.draw_guidelines)
        self.root.bind("<Configure>", self.on_window_resize)
        self.root.bind("<Control-0>", lambda event: self.reset_zoom())
        self.root.bind("<d>", lambda e: self.next_image())
        self.root.bind("<a>", lambda e: self.prev_image())
        self.root.bind("<w>", lambda e: self.enter_draw_mode_from_key())

    def enter_draw_mode_from_key(self):
        self.mode_var.set("draw")
        self.set_draw_mode()

    def reset_zoom(self):
        self.zoom_level = 1.0
        self.scale_factor = 1.0
        self.scale_image_to_fit()  # this handles image resizing and annotation redraw

    def on_mousewheel(self, event):
        # Normalize scroll direction
        if event.num == 5 or event.delta < 0:
            direction = -1
        elif event.num == 4 or event.delta > 0:
            direction = 1
        else:
            return

        # Define smooth step
        zoom_step = 1.03
        proposed_zoom = self.zoom_level * (zoom_step if direction > 0 else 1 / zoom_step)

        # Clamp to limits
        proposed_zoom = max(self.min_scale_factor, min(proposed_zoom, 5.0))

        # Calculate effective factor
        factor = proposed_zoom / self.zoom_level
        self.zoom_level = proposed_zoom
        self.scale_factor = proposed_zoom

        self.zoom_image(factor, event.x, event.y)


    def on_middle_click(self, event):
        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def on_middle_drag(self, event):

        if self.zoom_level <= self.min_scale_factor:
            return  # No panning when fully zoomed out

        dx = event.x - self.pan_start_x
        dy = event.y - self.pan_start_y

        # Get current scroll position (0.0 to 1.0)
        x0 = self.canvas.xview()[0]
        y0 = self.canvas.yview()[0]

        # Get scrollable size in screen pixels
        scroll_width = self.canvas.bbox("all")[2] - self.canvas.winfo_width()
        scroll_height = self.canvas.bbox("all")[3] - self.canvas.winfo_height()

        # Avoid division by zero
        if scroll_width > 0:
            new_x = x0 - dx / scroll_width
            self.canvas.xview_moveto(new_x)
        if scroll_height > 0:
            new_y = y0 - dy / scroll_height
            self.canvas.yview_moveto(new_y)

        self.pan_start_x = event.x
        self.pan_start_y = event.y


    def zoom_image(self, factor, center_x, center_y):
        if not self.original_image:
            return

        # Proposed zoom
        new_zoom = self.zoom_level * factor

        # Clamp limits
        if new_zoom < self.min_scale_factor:
            new_zoom = self.min_scale_factor
            factor = self.min_scale_factor / self.zoom_level
        elif new_zoom > 5.0:
            new_zoom = 5.0
            factor = 5.0 / self.zoom_level

        self.zoom_level = new_zoom
        self.scale_factor = new_zoom

        # Mouse position in canvas
        canvas_mouse_x = self.canvas.canvasx(center_x)
        canvas_mouse_y = self.canvas.canvasy(center_y)

        # Relative position in the image before zoom
        rel_x = (canvas_mouse_x - self.x_offset) / (self.original_image.width * (1 / factor) * self.scale_factor)
        rel_y = (canvas_mouse_y - self.y_offset) / (self.original_image.height * (1 / factor) * self.scale_factor)

        # Resize image
        new_width = int(self.original_image.width * self.scale_factor)
        new_height = int(self.original_image.height * self.scale_factor)

        if new_width > 10000 or new_height > 10000:
            print("Zoom limit hit: image would be too large")
            return

        self.current_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(self.current_image)

        # Clear canvas and set new scroll region
        self.canvas.delete("all")
        self.canvas.config(scrollregion=(0, 0, new_width, new_height))

        # New offset so image zooms around cursor
        self.x_offset = canvas_mouse_x - rel_x * new_width
        self.y_offset = canvas_mouse_y - rel_y * new_height

        # Draw image
        self.canvas.create_image(self.x_offset, self.y_offset, anchor=tk.NW, image=self.tk_image)

        # Redraw boxes
        self.draw_existing_annotations()



    def update_annotation_format(self):
        for fmt in self.annotation_formats:
            self.annotation_formats[fmt] = self.format_vars[fmt].get()

    def on_window_resize(self, event):
        if self.original_image:
            self.scale_image_to_fit()

    def set_select_mode(self):
        self.mode = "select"
        self.canvas.config(cursor="fleur")
        self.clear_guidelines()

    def set_draw_mode(self):
        if not self.class_var.get() or self.class_var.get() == "Select Class":
            messagebox.showerror("Error", "Please select a class first!")
            self.mode_var.set("select")
            return
        self.mode = "draw"
        self.current_class = self.class_var.get()
        self.canvas.config(cursor="crosshair")

    def draw_guidelines(self, event):
        self.clear_guidelines()

        # Get canvas coordinates accounting for pan/zoom
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        scroll_x0 = self.canvas.canvasx(0)
        scroll_x1 = self.canvas.canvasx(self.canvas.winfo_width())
        scroll_y0 = self.canvas.canvasy(0)
        scroll_y1 = self.canvas.canvasy(self.canvas.winfo_height())

        vert_guideline = self.canvas.create_line(
            x, scroll_y0, x, scroll_y1,
            fill="red", dash=(2, 2), width=1, tags="guideline"
        )

        horiz_guideline = self.canvas.create_line(
            scroll_x0, y, scroll_x1, y,
            fill="red", dash=(2, 2), width=1, tags="guideline"
        )

        self.guidelines = [vert_guideline, horiz_guideline]


    def clear_guidelines(self):
        for guideline in self.guidelines:
            self.canvas.delete(guideline)
        self.guidelines = []

    def ask_for_paths(self):
        self.image_folder = filedialog.askdirectory(title="Select Image Folder")
        if not self.image_folder:
            messagebox.showerror("Error", "No image folder selected!")
            return

        self.class_file = filedialog.askopenfilename(
            title="Select Class File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if self.class_file:
            self.load_classes()
        else:
            create = messagebox.askyesno("Class File", "No class file selected. Create new one?")
            if create:
                self.create_class_file()

        self.load_images()

    def open_image_folder(self):
        self.image_folder = filedialog.askdirectory(title="Select Image Folder")
        if self.image_folder:
            self.load_images()

    def open_class_file(self):
        self.class_file = filedialog.askopenfilename(
            title="Select Class File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if self.class_file:
            self.load_classes()

    def create_class_file(self):
        classes = simpledialog.askstring("Create Class File", "Enter class names separated by commas:")
        if classes:
            self.classes = [c.strip() for c in classes.split(",")]
            self.class_file = os.path.join(self.image_folder, "classes.txt")
            with open(self.class_file, 'w') as f:
                f.write("\n".join(self.classes))

            self.generate_colors()
            self.update_class_dropdown()

            messagebox.showinfo("Success", f"Class file created at {self.class_file}")

    def load_classes(self):
        try:
            with open(self.class_file, 'r') as f:
                self.classes = [line.strip() for line in f.readlines() if line.strip()]

            self.generate_colors()
            self.update_class_dropdown()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load class file: {str(e)}")

    def generate_colors(self):
        self.colors = []
        for i in range(len(self.classes)):
            hue = i / len(self.classes)
            rgb = colorsys.hsv_to_rgb(hue, 1, 1)
            self.colors.append("#%02x%02x%02x" % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)))

    def update_class_dropdown(self):
        menu = self.class_dropdown["menu"]
        menu.delete(0, "end")

        for cls in self.classes:
            menu.add_command(label=cls, command=lambda v=cls: self.class_var.set(v))

        if self.classes:
            self.class_var.set(self.classes[0])

    def load_images(self):
        if not self.image_folder:
            return

        extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
        self.images = [
            os.path.join(self.image_folder, f)
            for f in os.listdir(self.image_folder)
            if f.lower().endswith(extensions)
        ]

        if not self.images:
            messagebox.showerror("Error", "No images found in the selected folder!")
            return

        self.current_image_index = 0
        self.load_current_image()

    def load_current_image(self):
        if not self.images or self.current_image_index >= len(self.images):
            return

        image_path = self.images[self.current_image_index]

        # Load image and handle orientation properly
        self.original_image = Image.open(image_path)

        # Apply EXIF transpose to correct orientation without rotating
        try:
            from PIL import ImageOps
            self.original_image = ImageOps.exif_transpose(self.original_image)
        except (AttributeError, ImportError, KeyError):
            # Fallback if EXIF handling fails
            pass

        # Load annotations if they exist
        self.load_annotations_for_current_image()

        self.scale_image_to_fit()

        # Load annotations if they exist
        self.load_annotations_for_current_image()

        # Update annotations list
        self.update_annotations_list()

        # Update window title
        self.root.title(f"An-Augmenter - (Image Annotation and Data Augmentation Tool) - {os.path.basename(image_path)} ({self.current_image_index+1}/{len(self.images)})")

    def scale_image_to_fit(self):
        if not self.original_image:
            return

        canvas_width = self.image_frame.winfo_width() - 20
        canvas_height = self.image_frame.winfo_height() - 20

        if canvas_width <= 0 or canvas_height <= 0:
            return

        img_width, img_height = self.original_image.size
        width_ratio = canvas_width / img_width
        height_ratio = canvas_height / img_height
        fit_scale = min(width_ratio, height_ratio)
        self.scale_factor = fit_scale
        self.min_scale_factor = fit_scale
        self.zoom_level = fit_scale  # VERY IMPORTANT


        new_width = int(img_width * self.scale_factor)
        new_height = int(img_height * self.scale_factor)
        self.current_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(self.current_image)

        # Calculate offsets for centering
        self.x_offset = (canvas_width - new_width) / 2
        self.y_offset = (canvas_height - new_height) / 2

        self.canvas.delete("all")
        self.canvas.config(scrollregion=(0, 0, new_width, new_height))
        self.canvas.create_image(self.x_offset, self.y_offset, anchor=tk.NW, image=self.tk_image)
        self.min_scale_factor = self.scale_factor



        self.draw_existing_annotations()

    def load_annotations_for_current_image(self):
        image_path = self.images[self.current_image_index]
        annotation_path = os.path.splitext(image_path)[0] + ".txt"

        self.annotations[image_path] = []
        self.current_bbox_ids = []
        self.selected_annotation_index = None

        if os.path.exists(annotation_path):
            with open(annotation_path, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        class_id = int(parts[0])
                        x_center = float(parts[1])
                        y_center = float(parts[2])
                        width = float(parts[3])
                        height = float(parts[4])

                        img_width, img_height = self.original_image.size
                        x1 = (x_center - width/2) * img_width
                        y1 = (y_center - height/2) * img_height
                        x2 = (x_center + width/2) * img_width
                        y2 = (y_center + height/2) * img_height

                        self.annotations[image_path].append({
                            "class_id": class_id,
                            "class_name": self.classes[class_id],
                            "x1": x1,
                            "y1": y1,
                            "x2": x2,
                            "y2": y2
                        })

    def draw_existing_annotations(self):
        if not self.original_image:
            return

        image_path = self.images[self.current_image_index]
        self.current_bbox_ids = []

        for i, ann in enumerate(self.annotations[image_path]):
            x1 = ann["x1"] * self.scale_factor + self.x_offset
            y1 = ann["y1"] * self.scale_factor + self.y_offset
            x2 = ann["x2"] * self.scale_factor + self.x_offset
            y2 = ann["y2"] * self.scale_factor + self.y_offset

            color = self.colors[ann["class_id"]]
            rect_id = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                outline=color, width=2, tags="annotation"
            )

            label_text = ann["class_name"]
            font = ("Helvetica", 10)
            padding = 4

            # Measure text size by creating a temporary text item
            tmp_id = self.canvas.create_text(0, 0, text=label_text, font=font)
            bbox = self.canvas.bbox(tmp_id)
            self.canvas.delete(tmp_id)

            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # Default position above the box
            bg_x1 = x1-1
            bg_y1 = y1 - text_height - 2 * padding
            # If not enough space above, move below the box
            if bg_y1 < 0:
                bg_y1 = y1 + 2

            bg_x2 = bg_x1 + text_width + 2 * padding
            bg_y2 = bg_y1 + text_height + 2 * padding

            # Background rectangle for text
            text_bg = self.canvas.create_rectangle(
                bg_x1, bg_y1, bg_x2, bg_y2,
                fill=color, outline=color, tags="annotation"
            )

            # Label text
            text_id = self.canvas.create_text(
                bg_x1 + padding, bg_y1 + padding,
                text=label_text,
                anchor=tk.NW,
                fill="black",
                font=font,
                tags="annotation"
            )

            self.current_bbox_ids.append((rect_id, text_id, ann))

            if i == self.selected_annotation_index:
                self.canvas.itemconfig(rect_id, width=4)
                self.canvas.itemconfig(text_id, fill="white")


    def update_annotations_list(self):
        self.annotations_list.delete(0, tk.END)
        image_path = self.images[self.current_image_index]
        for i, ann in enumerate(self.annotations[image_path]):
            self.annotations_list.insert(tk.END,
                f"{i+1}: {ann['class_name']} ({ann['x1']:.1f}, {ann['y1']:.1f}) - ({ann['x2']:.1f}, {ann['y2']:.1f})")

        if self.selected_annotation_index is not None and self.selected_annotation_index < self.annotations_list.size():
            self.annotations_list.selection_set(self.selected_annotation_index)

    def on_annotation_select(self, event):
        if not self.annotations_list.curselection():
            self.selected_annotation_index = None
            return

        selected_index = self.annotations_list.curselection()[0]
        image_path = self.images[self.current_image_index]

        if selected_index < len(self.annotations[image_path]):
            self.selected_annotation_index = selected_index
            self.highlight_annotation(selected_index)

    def highlight_annotation(self, index):
        for i, (rect_id, text_id, ann) in enumerate(self.current_bbox_ids):
            self.canvas.itemconfig(rect_id, width=2)
            # Restore all text fills to black
            self.canvas.itemconfig(text_id, fill="black")

        if index < len(self.current_bbox_ids):
            self.canvas.itemconfig(self.current_bbox_ids[index][0], width=4)
            self.canvas.itemconfig(self.current_bbox_ids[index][1], fill="white")
            self.canvas.tag_raise(self.current_bbox_ids[index][0])
            self.canvas.tag_raise(self.current_bbox_ids[index][1])

    def delete_selected(self):
        image_path = self.images[self.current_image_index]

        if self.selected_annotation_index is None:
            messagebox.showwarning("Warning", "No annotation selected to delete!")
            return

        if self.selected_annotation_index < len(self.annotations[image_path]):
            del self.annotations[image_path][self.selected_annotation_index]
            self.selected_annotation_index = None
            self.annotations_list.selection_clear(0, tk.END)

            self.update_annotations_list()
            self.redraw_image_and_annotations()

    def redraw_image_and_annotations(self):
        # Resize the current image (based on current zoom)
        new_width = int(self.original_image.width * self.scale_factor)
        new_height = int(self.original_image.height * self.scale_factor)

        self.current_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(self.current_image)

        # Redraw the image
        self.canvas.delete("all")
        self.canvas.config(scrollregion=(0, 0, new_width, new_height))
        self.canvas.create_image(self.x_offset, self.y_offset, anchor=tk.NW, image=self.tk_image)

        # Then redraw bounding boxes
        self.draw_existing_annotations()


    def prev_image(self):
        if self.current_image_index > 0:
            self.save_current_annotations(only_if_annotations=True)
            self.current_image_index -= 1
            self.load_current_image()

    def next_image(self):
        if self.current_image_index < len(self.images) - 1:
            self.save_current_annotations(only_if_annotations=True)
            self.current_image_index += 1
            self.load_current_image()
        else:
            messagebox.showinfo("Info", "You've reached the last image.")

    def on_mouse_press(self, event):
        if self.mode == "draw":
            self.drawing = True
            self.start_x = self.canvas.canvasx(event.x) - self.x_offset
            self.start_y = self.canvas.canvasy(event.y) - self.y_offset
            self.rect = self.canvas.create_rectangle(
                self.start_x + self.x_offset,
                self.start_y + self.y_offset,
                self.start_x + self.x_offset,
                self.start_y + self.y_offset,
                outline="red", width=2
            )

        elif self.mode == "select":
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)

            found = False
            for i, (rect_id, text_id, ann) in enumerate(self.current_bbox_ids):
                coords = self.canvas.coords(rect_id)
                if coords[0] <= x <= coords[2] and coords[1] <= y <= coords[3]:
                    self.selected_annotation_index = i
                    self.annotations_list.selection_clear(0, tk.END)
                    self.annotations_list.selection_set(i)
                    self.highlight_annotation(i)
                    found = True
                    break

            if not found:
                # Clear any previous selection if click is outside all boxes
                self.selected_annotation_index = None
                self.annotations_list.selection_clear(0, tk.END)
                self.draw_existing_annotations()


    def on_mouse_drag(self, event):
        if self.drawing and self.rect:
            x = self.canvas.canvasx(event.x) - self.x_offset
            y = self.canvas.canvasy(event.y) - self.y_offset
            self.canvas.coords(
                self.rect,
                self.start_x + self.x_offset,
                self.start_y + self.y_offset,
                x + self.x_offset,
                y + self.y_offset
            )

    def on_mouse_release(self, event):
        if self.drawing and self.rect:
            self.drawing = False
            end_x = self.canvas.canvasx(event.x) - self.x_offset
            end_y = self.canvas.canvasy(event.y) - self.y_offset

            # Convert back to original image coordinates
            orig_x1 = self.start_x / self.scale_factor
            orig_y1 = self.start_y / self.scale_factor
            orig_x2 = end_x / self.scale_factor
            orig_y2 = end_y / self.scale_factor

            # Ensure coordinates are within image bounds
            img_width, img_height = self.original_image.size
            x1 = max(0, min(orig_x1, orig_x2))
            y1 = max(0, min(orig_y1, orig_y2))
            x2 = min(img_width, max(orig_x1, orig_x2))
            y2 = min(img_height, max(orig_y1, orig_y2))

            if abs(x2 - x1) > 5 and abs(y2 - y1) > 5:
                self.pending_box = (x1, y1, x2, y2)
                self.show_class_selection_popup(event.x_root, event.y_root)

            self.canvas.delete(self.rect)
            self.rect = None

            self.mode_var.set("select")
            self.mode = "select"

# ------------------------------------------------------------------------------------------------------------------------

    def show_class_selection_popup(self, x, y):
        popup = tk.Toplevel(self.root)
        popup.wm_overrideredirect(True)
        popup.geometry(f"+{x}+{y}")
        popup.config(bg="white", borderwidth=2)

        tk.Label(popup, text="Select Class:", bg="white").pack()

        for cls in self.classes:
            btn = tk.Button(popup, text=cls, command=lambda c=cls, p=popup: self.assign_class_to_pending_box(c, p))
            btn.pack(fill="x")

    def assign_class_to_pending_box(self, selected_class, popup_window):
        popup_window.destroy()
        if not self.pending_box:
            return

        x1, y1, x2, y2 = self.pending_box
        self.pending_box = None
        image_path = self.images[self.current_image_index]
        class_id = self.classes.index(selected_class)

        self.annotations[image_path].append({
            "class_id": class_id,
            "class_name": selected_class,
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2
        })

        self.update_annotations_list()
        self.draw_existing_annotations()

# ----------------------------------------------------------------------------------------------------------------------------------

    def save_current_annotations(self, only_if_annotations=False):
        if not self.images or self.current_image_index >= len(self.images):
            return

        image_path = self.images[self.current_image_index]
        base_path = os.path.splitext(image_path)[0]
        img_width, img_height = self.original_image.size

        annotations = self.annotations[image_path]

        if only_if_annotations and not annotations:
            # Remove all formats if they exist
            for ext in [".txt", ".json", ".xml"]:
                ann_path = base_path + ext
                if os.path.exists(ann_path):
                    os.remove(ann_path)
            return

        # Prepare YOLO format data
        yolo_annotations = []
        for ann in annotations:
            x_center = ((ann["x1"] + ann["x2"]) / 2) / img_width
            y_center = ((ann["y1"] + ann["y2"]) / 2) / img_height
            width = (ann["x2"] - ann["x1"]) / img_width
            height = (ann["y2"] - ann["y1"]) / img_height
            yolo_annotations.append(f"{ann['class_id']} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

        # Save YOLO format
        if self.annotation_formats.get("yolo", False):
            with open(base_path + ".txt", 'w') as f:
                f.write("\n".join(yolo_annotations))

        # Save JSON format
        if self.annotation_formats.get("json", False):
            with open(base_path + ".json", 'w') as f:
                json.dump(annotations, f, indent=4)

        # Save XML format (Pascal VOC)
        if self.annotation_formats.get("xml", False):
            root = ET.Element("annotation")
            ET.SubElement(root, "filename").text = os.path.basename(image_path)

            size = ET.SubElement(root, "size")
            ET.SubElement(size, "width").text = str(img_width)
            ET.SubElement(size, "height").text = str(img_height)
            ET.SubElement(size, "depth").text = "3"

            for ann in annotations:
                obj = ET.SubElement(root, "object")
                ET.SubElement(obj, "name").text = ann["class_name"]
                bbox = ET.SubElement(obj, "bndbox")
                ET.SubElement(bbox, "xmin").text = str(int(ann["x1"]))
                ET.SubElement(bbox, "ymin").text = str(int(ann["y1"]))
                ET.SubElement(bbox, "xmax").text = str(int(ann["x2"]))
                ET.SubElement(bbox, "ymax").text = str(int(ann["y2"]))

            tree = ET.ElementTree(root)
            tree.write(base_path + ".xml")

    def setup_augmentation_ui(self):
        """Create the augmentation controls"""
        self.augmentation_panel = tk.Toplevel(self.root)
        self.augmentation_panel.title("Augmentation Settings")
        self.augmentation_panel.geometry("400x600")

        self.aug_params = {}
        self.aug_widgets = {}

        row = 0
        for aug_name, config in self.augmenter.augmentations.items():
            # Create checkbox for each augmentation
            var = tk.BooleanVar(value=False)
            cb = tk.Checkbutton(self.augmentation_panel, text=aug_name, variable=var)
            cb.grid(row=row, column=0, sticky="w")

            # Create slider for parameters if needed
            if "range" in config:
                min_val, max_val = config["range"]
                if isinstance(min_val, tuple):  # For tuple parameters like blur
                    default_val = config["default"][0]
                    scale = tk.Scale(self.augmentation_panel, from_=min_val[0], to=max_val[0],
                                    orient=tk.HORIZONTAL, label=f"{aug_name} value")
                    scale.set(default_val)
                    scale.grid(row=row, column=1)
                    self.aug_widgets[f"{aug_name}_value"] = scale
                else:  # For single value parameters
                    scale = tk.Scale(self.augmentation_panel, from_=min_val, to=max_val,
                                    orient=tk.HORIZONTAL, label=f"{aug_name} value")
                    scale.set(config["default"])
                    scale.grid(row=row, column=1)
                    self.aug_widgets[f"{aug_name}_value"] = scale

            self.aug_widgets[aug_name] = var
            row += 1

        # Add apply button
        tk.Button(self.augmentation_panel, text="Apply Augmentations",
                command=self.apply_augmentations).grid(row=row, columnspan=2)

    # Add this method to your ImageAnnotator class:
    def setup_augmentation_ui(self):
        """Create the augmentation controls with proper sliders"""
        self.augmentation_panel = tk.Toplevel(self.root)
        self.augmentation_panel.title("Augmentation Settings")
        self.augmentation_panel.geometry("500x800")

        self.aug_params = {}
        self.aug_widgets = {}

        # Create a canvas and scrollbar for the panel
        canvas = tk.Canvas(self.augmentation_panel)
        scrollbar = tk.Scrollbar(self.augmentation_panel, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        row = 0
        for aug_name, config in self.augmenter.augmentations.items():
            # Frame for each augmentation control
            frame = tk.Frame(scrollable_frame)
            frame.grid(row=row, column=0, sticky="ew", padx=5, pady=5)

            # Checkbox for enabling the augmentation
            var = tk.BooleanVar(value=False)
            cb = tk.Checkbutton(frame, text=aug_name, variable=var)
            cb.pack(side="left", anchor="w")
            self.aug_widgets[aug_name] = var

            # Slider for parameters if needed
            if "range" in config:
                min_val, max_val = config["range"]
                default_val = config["default"]

                # Create appropriate slider based on parameter type
                if isinstance(min_val, tuple) and aug_name == "zoom":  # For tuple parameters like blur
                    # First value slider
                    frame_val1 = tk.Frame(scrollable_frame)
                    frame_val1.grid(row=row+1, column=0, sticky="ew", padx=20)

                    lbl1 = tk.Label(frame_val1, text=f"{aug_name} value 1")
                    lbl1.pack(side="left")

                    scale1 = tk.Scale(
                        frame_val1,
                        from_=min_val[0],
                        to=max_val[0],
                        resolution=0.1 if isinstance(default_val[0], float) else 1,
                        orient=tk.HORIZONTAL
                    )
                    scale1.set(default_val[0])
                    scale1.pack(side="left", fill="x", expand=True)
                    self.aug_widgets[f"{aug_name}_value1"] = scale1

                    # Second value slider
                    frame_val2 = tk.Frame(scrollable_frame)
                    frame_val2.grid(row=row+2, column=0, sticky="ew", padx=20)

                    lbl2 = tk.Label(frame_val2, text=f"{aug_name} value 2")
                    lbl2.pack(side="left")

                    scale2 = tk.Scale(
                        frame_val2,
                        from_=min_val[1],
                        to=max_val[1],
                        resolution=0.1 if isinstance(default_val[1], float) else 1,
                        orient=tk.HORIZONTAL
                    )
                    scale2.set(default_val[1])
                    scale2.pack(side="left", fill="x", expand=True)
                    self.aug_widgets[f"{aug_name}_value2"] = scale2

                    row += 2
                else:  # For single value parameters
                    frame_val = tk.Frame(scrollable_frame)
                    frame_val.grid(row=row+1, column=0, sticky="ew", padx=20)

                    lbl = tk.Label(frame_val, text=f"{aug_name} value")
                    lbl.pack(side="left")

                    scale = tk.Scale(
                        frame_val,
                        from_=min_val,
                        to=max_val,
                        resolution=0.1 if isinstance(default_val, float) else 1,
                        orient=tk.HORIZONTAL
                    )
                    scale.set(default_val)
                    scale.pack(side="left", fill="x", expand=True)
                    self.aug_widgets[f"{aug_name}_value"] = scale

                    row += 1

            row += 1

        # --- Format selection for augmentation ---
        format_frame = tk.LabelFrame(scrollable_frame, text="Save Annotation Formats", bg="white", padx=10, pady=5)
        format_frame.grid(row=row, column=0, sticky="ew", pady=10)

        self.aug_format_vars = {
            "yolo": tk.BooleanVar(value=self.annotation_formats.get("yolo", True)),
            "json": tk.BooleanVar(value=self.annotation_formats.get("json", False)),
            "xml": tk.BooleanVar(value=self.annotation_formats.get("xml", False)),
        }

        for fmt in ["yolo", "json", "xml"]:
            tk.Checkbutton(
                format_frame, text=fmt.upper(), variable=self.aug_format_vars[fmt],
                bg='white', anchor="w"
            ).pack(anchor="w")


        # Add apply button at the bottom
        btn_frame = tk.Frame(scrollable_frame)
        btn_frame.grid(row=row+1, column=0, pady=10)

        tk.Button(
            btn_frame,
            text="Apply Augmentations",
            command=self.apply_augmentations
        ).pack()

    # def apply_augmentations(self):
    #     output_dir = filedialog.askdirectory(title="Select Output Directory for Augmented Images")
    #     if not output_dir:
    #         return

    #     params = {}
    #     aug_multiplier = 0

    #     for aug_name in self.augmenter.augmentations:
    #         if self.aug_widgets[aug_name].get():
    #             params[aug_name] = True
    #             config = self.augmenter.augmentations[aug_name]

    #             if "range" in config:
    #                 if isinstance(config["range"][0], tuple):
    #                     val1 = self.aug_widgets[f"{aug_name}_value1"].get()
    #                     val2 = self.aug_widgets[f"{aug_name}_value2"].get()
    #                     params[f"{aug_name}_value"] = (val1, val2)
    #                 else:
    #                     val = self.aug_widgets[f"{aug_name}_value"].get()
    #                     params[f"{aug_name}_value"] = val

    #             aug_multiplier += 1

    #     if not params:
    #         messagebox.showwarning("Warning", "No augmentations selected!")
    #         return

    #     formats = {fmt: var.get() for fmt, var in self.aug_format_vars.items()}

    #     # Flag to handle early stopping
    #     self.stop_augmentation = False

    #     # Create a moveable and interruptible progress window
    #     progress_win = tk.Toplevel(self.root)
    #     progress_win.title("Augmenting Images")
    #     progress_win.geometry("450x150")
    #     progress_win.transient(self.root)
    #     progress_win.grab_set()

    #     def on_close():
    #         if messagebox.askyesno("Stop?", "Do you want to stop augmentation?"):
    #             self.stop_augmentation = True

    #     progress_win.protocol("WM_DELETE_WINDOW", on_close)

    #     tk.Label(progress_win, text="Augmenting images...").pack(pady=5)

    #     bar_var = tk.DoubleVar()
    #     progress_bar = ttk.Progressbar(progress_win, maximum=100, length=350, variable=bar_var)
    #     progress_bar.pack(pady=5)

    #     label_image = tk.Label(progress_win, text="")
    #     label_image.pack()

    #     label_aug = tk.Label(progress_win, text="")
    #     label_aug.pack()

    #     self.root.update_idletasks()

    #     total_images = len(self.images)
    #     total_aug_images = total_images * aug_multiplier
    #     current_aug_count = 0

    #     for img_idx, image_path in enumerate(self.images, start=1):
    #         if self.stop_augmentation:
    #             break

    #         label_image.config(text=f"Processing image {img_idx} of {total_images}")
    #         self.root.update_idletasks()

    #         try:
    #             img = Image.open(image_path)
    #             img = ImageOps.exif_transpose(img)
    #         except Exception as e:
    #             print(f"Warning: Failed to open/transpose {image_path}: {e}")
    #             continue

    #         width, height = img.size
    #         annotation_path = os.path.splitext(image_path)[0] + ".txt"
    #         bboxes = None
    #         if os.path.exists(annotation_path):
    #             bboxes = self.augmenter.read_yolo_annotations(annotation_path, width, height)

    #         generated_paths = self.augmenter.apply_augmentations(
    #             image_path, output_dir, params, bboxes, formats=formats, class_list=self.classes
    #         )

    #         if isinstance(generated_paths, list):
    #             generated_count = len(generated_paths)
    #         else:
    #             generated_count = aug_multiplier

    #         for i in range(generated_count):
    #             if self.stop_augmentation:
    #                 break

    #             current_aug_count += 1
    #             percent = int((current_aug_count / total_aug_images) * 100)
    #             label_aug.config(text=f"Generating augmentation {current_aug_count} of {total_aug_images} ({percent}%)")
    #             bar_var.set(percent)
    #             self.root.update_idletasks()

    #     progress_win.destroy()
    #     self.augmentation_panel.destroy()

        # if self.stop_augmentation:
        #     messagebox.showinfo("Stopped", f"Augmentation stopped early.\nPartial results saved in:\n{output_dir}")
        # else:
        #     messagebox.showinfo("Success", f"Augmented images saved to:\n{output_dir}")

    def apply_augmentations(self):
        output_dir = filedialog.askdirectory(title="Select Output Directory for Augmented Images")
        if not output_dir:
            return

        params = {}
        aug_multiplier = 0

        for aug_name in self.augmenter.augmentations:
            if self.aug_widgets[aug_name].get():
                params[aug_name] = True
                config = self.augmenter.augmentations[aug_name]

                if "range" in config:
                    if isinstance(config["range"][0], tuple):
                        val1 = self.aug_widgets[f"{aug_name}_value1"].get()
                        val2 = self.aug_widgets[f"{aug_name}_value2"].get()
                        params[f"{aug_name}_value"] = (val1, val2)
                    else:
                        val = self.aug_widgets[f"{aug_name}_value"].get()
                        params[f"{aug_name}_value"] = val

                aug_multiplier += 1

        if not params:
            messagebox.showwarning("Warning", "No augmentations selected!")
            return

        formats = {fmt: var.get() for fmt, var in self.aug_format_vars.items()}
        self.stop_augmentation = False

        # Open progress window (handled on main thread)
        self.progress_win = tk.Toplevel(self.root)
        self.progress_win.title("Augmenting Images")
        self.progress_win.geometry("450x150")
        self.progress_win.transient(self.root)

        self.bar_var = tk.DoubleVar()
        tk.Label(self.progress_win, text="Augmenting images...").pack(pady=5)
        self.progress_bar = ttk.Progressbar(self.progress_win, maximum=100, length=350, variable=self.bar_var)
        self.progress_bar.pack(pady=5)
        self.label_image = tk.Label(self.progress_win, text="")
        self.label_image.pack()
        self.label_aug = tk.Label(self.progress_win, text="")
        self.label_aug.pack()

        def on_close():
            if messagebox.askyesno("Stop?", "Do you want to stop augmentation?"):
                self.stop_augmentation = True

        self.progress_win.protocol("WM_DELETE_WINDOW", on_close)

        # Start worker thread
        thread = threading.Thread(target=self._run_augmentation_thread, args=(params, formats, output_dir, aug_multiplier))
        thread.start()

    def _run_augmentation_thread(self, params, formats, output_dir, aug_multiplier):
        try:
            total_images = len(self.images)
            total_aug_images = total_images * aug_multiplier
            current_aug_count = 0

            for img_idx, image_path in enumerate(self.images, start=1):
                if self.stop_augmentation:
                    break

                self.label_image.config(text=f"Processing image {img_idx} of {total_images}")
                self.root.update_idletasks()

                try:
                    img = Image.open(image_path)
                    img = ImageOps.exif_transpose(img)
                except Exception as e:
                    print(f"Warning: Failed to open/transpose {image_path}: {e}")
                    continue

                width, height = img.size
                annotation_path = os.path.splitext(image_path)[0] + ".txt"
                bboxes = None
                if os.path.exists(annotation_path):
                    bboxes = self.augmenter.read_yolo_annotations(annotation_path, width, height)

                generated_paths = self.augmenter.apply_augmentations(
                    image_path, output_dir, params, bboxes, formats=formats, class_list=self.classes
                )

                generated_count = len(generated_paths) if isinstance(generated_paths, list) else aug_multiplier

                for _ in range(generated_count):
                    if self.stop_augmentation:
                        break
                    current_aug_count += 1
                    percent = int((current_aug_count / total_aug_images) * 100)
                    self.bar_var.set(percent)
                    self.label_aug.config(text=f"Generating augmentation {current_aug_count} of {total_aug_images} ({percent}%)")
                    self.root.update_idletasks()

            self.progress_win.destroy()
            self.augmentation_panel.destroy()

            if self.stop_augmentation:
                messagebox.showinfo("Stopped", f"Augmentation stopped early.\nPartial results saved in:\n{output_dir}")
            else:
                messagebox.showinfo("Success", f"Augmented images saved to:\n{output_dir}")

        except Exception as e:
            print(f"Error during augmentation: {e}")
            messagebox.showerror("Error", str(e))




if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x800")

    def start_main_gui():
        for widget in root.winfo_children():
            widget.destroy()
        app = ImageAnnotator(root)

    WelcomeScreen(root, start_main_gui)
    root.mainloop()
