import cv2
import numpy as np
import matplotlib.pyplot as plt

def load_yolo_labels(label_path, img_width, img_height):
    bboxes = []
    with open(label_path, 'r') as f:
        for line in f:
            class_id, x_center, y_center, width, height = map(float, line.strip().split())
            # Convert from YOLO format to pixel (x_min, y_min, x_max, y_max)
            x_center *= img_width
            y_center *= img_height
            width *= img_width
            height *= img_height

            x_min = x_center - width / 2
            y_min = y_center - height / 2
            x_max = x_center + width / 2
            y_max = y_center + height / 2
            bboxes.append([x_min, y_min, x_max, y_max, int(class_id)])
    return np.array(bboxes)

def flip_yolo_bboxes(bboxes, img_width):
    flipped_bboxes = bboxes.copy()
    flipped_bboxes[:, 0] = img_width - bboxes[:, 2]
    flipped_bboxes[:, 2] = img_width - bboxes[:, 0]
    return flipped_bboxes

def draw_bboxes(image, bboxes, color=(0, 255, 0), thickness=2):
    image_copy = image.copy()
    for bbox in bboxes:
        x_min, y_min, x_max, y_max, class_id = bbox
        cv2.rectangle(image_copy, (int(x_min), int(y_min)), (int(x_max), int(y_max)), color, thickness)
        cv2.putText(image_copy, str(class_id), (int(x_min), int(y_min) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    return image_copy

def visualize(original_image, flipped_image):
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(original_image)
    plt.title("Original Image")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(flipped_image)
    plt.title("Flipped Image")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

def convert_to_yolo_format(bboxes, img_width, img_height):
    yolo_labels = []
    for bbox in bboxes:
        x_min, y_min, x_max, y_max, class_id = bbox
        x_center = (x_min + x_max) / 2 / img_width
        y_center = (y_min + y_max) / 2 / img_height
        width = (x_max - x_min) / img_width
        height = (y_max - y_min) / img_height
        yolo_labels.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
    return yolo_labels

# Example usage
if __name__ == "__main__":
    image_path = "images/sam_combined (92).jpg"
    label_path = "images/sam_combined (92).txt"

    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_h, img_w = image.shape[:2]

    bboxes = load_yolo_labels(label_path, img_w, img_h)
    # print(bboxes)
    image_with_boxes = draw_bboxes(image, bboxes)

    flipped_image = cv2.flip(image, 1)
    flipped_bboxes = flip_yolo_bboxes(bboxes, img_w)
    print (flipped_bboxes)
    flipped_image_with_boxes = draw_bboxes(flipped_image, flipped_bboxes)
    visualize(image_with_boxes, flipped_image_with_boxes)

    # Optional: save flipped labels in YOLO format
    flipped_yolo_labels = convert_to_yolo_format(flipped_bboxes, img_w, img_h)
    with open("flipped_" + label_path, "w") as f:
        for line in flipped_yolo_labels:
            f.write(line + "\n")
