import cv2
import os
import albumentations as A
import matplotlib.pyplot as plt
from albumentations.pytorch import ToTensorV2

def read_yolo_labels(label_path, image_width, image_height):
    bboxes = []
    class_labels = []
    with open(label_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            class_id = int(parts[0])
            x_center, y_center, width, height = map(float, parts[1:])

            x_min = (x_center - width / 2) * image_width
            y_min = (y_center - height / 2) * image_height
            x_max = (x_center + width / 2) * image_width
            y_max = (y_center + height / 2) * image_height

            bboxes.append([x_min, y_min, x_max, y_max])
            class_labels.append(str(class_id))
    return bboxes, class_labels

def save_yolo_labels(output_path, bboxes, class_labels, image_width, image_height):
    with open(output_path, 'w') as f:
        for bbox, cls in zip(bboxes, class_labels):
            x_min, y_min, x_max, y_max = bbox
            x_center = (x_min + x_max) / 2 / image_width
            y_center = (y_min + y_max) / 2 / image_height
            width = (x_max - x_min) / image_width
            height = (y_max - y_min) / image_height
            f.write(f"{cls} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

def draw_boxes(image, bboxes, labels=None, color=(0, 255, 0)):
    image_with_boxes = image.copy()
    for i, (x_min, y_min, x_max, y_max) in enumerate(bboxes):
        cv2.rectangle(image_with_boxes, (int(x_min), int(y_min)), (int(x_max), int(y_max)), color, 2)
        if labels:
            cv2.putText(image_with_boxes, labels[i], (int(x_min), int(y_min)-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    return image_with_boxes

def apply_zoom_augmentation(image_path, label_path, output_image_path, output_label_path, scale_range=(1.1, 1.3)):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width = image.shape[:2]

    bboxes, class_labels = read_yolo_labels(label_path, width, height)

    transform = A.Compose([
        A.RandomScale(scale_limit=(scale_range[0]-1.0, scale_range[1]-1.0), p=1.0),
        A.PadIfNeeded(min_height=height, min_width=width, border_mode=cv2.BORDER_CONSTANT, value=[0,0,0]),
        A.RandomCrop(height=height, width=width),
    ], bbox_params=A.BboxParams(format='pascal_voc', label_fields=['class_labels']))

    augmented = transform(image=image, bboxes=bboxes, class_labels=class_labels)
    aug_img = augmented['image']
    aug_bboxes = augmented['bboxes']
    aug_labels = augmented['class_labels']

    # Save augmented image
    cv2.imwrite(output_image_path, cv2.cvtColor(aug_img, cv2.COLOR_RGB2BGR))
    save_yolo_labels(output_label_path, aug_bboxes, aug_labels, width, height)

    # Visualization
    original_img_with_boxes = draw_boxes(image, bboxes, class_labels, color=(0, 255, 0))
    augmented_img_with_boxes = draw_boxes(aug_img, aug_bboxes, aug_labels, color=(255, 0, 0))

    fig, axs = plt.subplots(1, 2, figsize=(14, 7))
    axs[0].imshow(original_img_with_boxes)
    axs[0].set_title('Original Image with BBoxes')
    axs[0].axis('off')

    axs[1].imshow(augmented_img_with_boxes)
    axs[1].set_title('Zoomed Image with Transformed BBoxes')
    axs[1].axis('off')

    plt.tight_layout()
    plt.show()

# ==== Example usage ====

image_path = "images\sam_combined (35).jpg"
label_path = "images\sam_combined (35).txt"  # YOLO format
output_image_path = "augmented/output_zoomed.jpg"
output_label_path = "augmented/output_zoomed.txt"
scale_range = (0.5, 0.5)  # 20% fixed zoom

apply_zoom_augmentation(image_path, label_path, output_image_path, output_label_path, scale_range)
