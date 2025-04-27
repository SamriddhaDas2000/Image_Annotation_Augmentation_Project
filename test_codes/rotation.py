import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

def yolo_to_voc(x_center, y_center, w, h, img_w, img_h):
    x_min = int((x_center - w / 2) * img_w)
    y_min = int((y_center - h / 2) * img_h)
    x_max = int((x_center + w / 2) * img_w)
    y_max = int((y_center + h / 2) * img_h)
    return x_min, y_min, x_max, y_max

def voc_to_yolo(x_min, y_min, x_max, y_max, img_w, img_h):
    x_center = ((x_min + x_max) / 2) / img_w
    y_center = ((y_min + y_max) / 2) / img_h
    w = (x_max - x_min) / img_w
    h = (y_max - y_min) / img_h
    return x_center, y_center, w, h

def rotate_image_and_boxes(image, boxes, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_img = cv2.warpAffine(image, M, (w, h))
    rotated_boxes = []
    for cls, x_min, y_min, x_max, y_max in boxes:
        corners = np.array([
            [x_min, y_min],
            [x_min, y_max],
            [x_max, y_min],
            [x_max, y_max]
        ])
        ones = np.ones((4, 1))
        corners_ones = np.hstack([corners, ones])
        transformed = M.dot(corners_ones.T).T
        x_coords = transformed[:, 0]
        y_coords = transformed[:, 1]
        new_x_min = int(np.clip(np.min(x_coords), 0, w - 1))
        new_y_min = int(np.clip(np.min(y_coords), 0, h - 1))
        new_x_max = int(np.clip(np.max(x_coords), 0, w - 1))
        new_y_max = int(np.clip(np.max(y_coords), 0, h - 1))
        rotated_boxes.append([cls, new_x_min, new_y_min, new_x_max, new_y_max])
    return rotated_img, rotated_boxes, w, h

def draw_boxes(image, boxes, color=(0, 255, 0)):
    image_with_boxes = image.copy()
    for cls, x_min, y_min, x_max, y_max in boxes:
        cv2.rectangle(image_with_boxes, (x_min, y_min), (x_max, y_max), color, 10)
    return image_with_boxes

def read_yolo_labels(label_path, img_w, img_h):
    boxes = []
    with open(label_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            cls = int(parts[0])
            x_c, y_c, w, h = map(float, parts[1:])
            x_min, y_min, x_max, y_max = yolo_to_voc(x_c, y_c, w, h, img_w, img_h)
            boxes.append([cls, x_min, y_min, x_max, y_max])
    return boxes

def write_yolo_labels(label_path, boxes, img_w, img_h):
    with open(label_path, 'w') as f:
        for cls, x_min, y_min, x_max, y_max in boxes:
            x_c, y_c, w, h = voc_to_yolo(x_min, y_min, x_max, y_max, img_w, img_h)
            f.write(f"{cls} {x_c:.6f} {y_c:.6f} {w:.6f} {h:.6f}\n")

def resize_image_keep_aspect(image, width=400):
    h, w = image.shape[:2]
    scale = width / w
    return cv2.resize(image, (width, int(h * scale)))

def main(image_path, angle):
    base = os.path.splitext(os.path.basename(image_path))[0]
    dir_path = os.path.dirname(image_path)
    label_path = os.path.join(dir_path, base + '.txt')

    image = cv2.imread(image_path)
    h, w = image.shape[:2]
    boxes = read_yolo_labels(label_path, w, h)

    rotated_img, rotated_boxes, new_w, new_h = rotate_image_and_boxes(image, boxes, angle)

    original_with_boxes = draw_boxes(image, boxes, color=(0, 255, 0))
    rotated_with_boxes = draw_boxes(rotated_img, rotated_boxes, color=(255, 0, 0))

    # Resize for display
    original_resized = resize_image_keep_aspect(original_with_boxes, width=500)
    rotated_resized = resize_image_keep_aspect(rotated_with_boxes, width=500)

    # Convert BGR to RGB for matplotlib
    original_rgb = cv2.cvtColor(original_resized, cv2.COLOR_BGR2RGB)
    rotated_rgb = cv2.cvtColor(rotated_resized, cv2.COLOR_BGR2RGB)

    # Show using matplotlib
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(original_rgb)
    plt.title("Original Image with Boxes")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(rotated_rgb)
    plt.title(f"Rotated Image ({angle}°) with Boxes")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

    # Save rotated image and labels
    new_img_path = os.path.join(dir_path, base + f'_rot{angle}.jpg')
    new_label_path = os.path.join(dir_path, base + f'_rot{angle}.txt')
    cv2.imwrite(new_img_path, rotated_img)
    write_yolo_labels(new_label_path, rotated_boxes, new_w, new_h)

    print(f"✅ Rotated image saved at: {new_img_path}")
    print(f"✅ Rotated labels saved at: {new_label_path}")
    print("📦 Final rotated bounding boxes (YOLO format):")
    for box in rotated_boxes:
        print(voc_to_yolo(box[1], box[2], box[3], box[4], new_w, new_h))

if __name__ == "__main__":
    image_path = "images/sam_combined (140).jpg"
    angle = 30
    main(image_path, angle)
