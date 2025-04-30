import cv2
import albumentations as A
import numpy as np
import os
import math
from PIL import Image
import random
import json
import xml.etree.ElementTree as ET


class ImageAugmenter:
    def __init__(self):
        self.augmentations = {
            "flip": {
                "func": lambda p: A.HorizontalFlip(p=1),
                "requires_bbox": False,
                "affects_bbox": True,
                "default": False,
                "transform_bbox": self.transform_flip_bbox
            },
            "rotate": {
                # "func": lambda x: A.Rotate(limit=x, p=1, border_mode=cv2.BORDER_CONSTANT),
                "func": self.sampled_rotate,
                "requires_bbox": False,
                "affects_bbox": True,
                "default": 30,
                "range": (-90, 90),
                "transform_bbox": self.transform_rotate_bbox
            },
            "blur": {
                "func": lambda x: A.GaussianBlur(blur_limit=x, p=1),
                "requires_bbox": False,
                "affects_bbox": False,
                "default": (3, 7),
                "range": ((1, 1), (15, 15))
            },
            "noise": {
                "func": lambda x: A.GaussNoise(std_range=(x,x), p=1),
                "requires_bbox": False,
                "affects_bbox": False,
                "default": 0.1,
                "range": (0.0, 1.0)
            },
            "brightness": {
                "func": lambda x: A.RandomBrightnessContrast(brightness_limit=x, p=1),
                "requires_bbox": False,
                "affects_bbox": False,
                "default": 0.2,
                "range": (0, 1)
            },
            "contrast": {
                "func": lambda x: A.RandomBrightnessContrast(contrast_limit=x, p=1),
                "requires_bbox": False,
                "affects_bbox": False,
                "default": 0.2,
                "range": (0, 1)
            },
            "hue": {
                "func": lambda x: A.HueSaturationValue(hue_shift_limit=x, p=1),
                "requires_bbox": False,
                "affects_bbox": False,
                "default": 20,
                "range": (0, 30)
            },
            "saturation": {
                "func": lambda x: A.HueSaturationValue(sat_shift_limit=x, p=1),
                "requires_bbox": False,
                "affects_bbox": False,
                "default": 30,
                "range": (0, 50)
            },
            "zoom": {
            "requires_bbox": False,  # Zoom requires bboxes to properly adjust them
            "affects_bbox": True,  # Zoom affects bboxes
            "default": (0.8, 1.2),  # Default zoom scale range
            "range": ((0.5, 0.5), (2.0, 2.0))  # Allowable zoom range
        }

        }

    # def transform_flip_bbox(self, bbox, img_width, img_height):
    #     """Correct horizontal flip transformation that works for all positions"""
    #     x_min, y_min, x_max, y_max, class_id = bbox
    #     # print(f"Original bbox (pixels): {bbox}")
    #     # print(f"Image dimensions: {img_width}x{img_height}")
    #     # Calculate mirrored coordinates (simple and mathematically correct)

    #     new_x_min = img_width - x_max
    #     new_x_max = img_width - x_min

    #     # Ensure coordinates are within image boundaries
    #     new_x_min = max(0, min(img_width, new_x_min))
    #     new_x_max = max(0, min(img_width, new_x_max))

    #     # print(f"Flipped bbox (pixels): {[new_x_min, y_min, new_x_max, y_max, class_id]}")


    #     return [new_x_min, y_min, new_x_max, y_max, class_id]

    def sampled_rotate(self, max_limit):
        self.last_sampled_angle = random.uniform(-max_limit, max_limit)
        # print(f"Sampled Rotation Angle: {self.last_sampled_angle}")  # or store it if needed
        return A.Rotate(limit=(self.last_sampled_angle, self.last_sampled_angle), p=1, border_mode=cv2.BORDER_CONSTANT)


    def transform_flip_bbox(self, bbox, img_width, img_height):
        """Correct horizontal flip transformation using center-mirroring logic"""
        x_min, y_min, x_max, y_max, class_id = bbox

        # Calculate image center (horizontal only)
        center_x = img_width / 2

        # Mirror x_min and x_max across the image center
        new_x_min = 2 * center_x - x_max
        new_x_max = 2 * center_x - x_min

        # Ensure x_min is less than x_max after flipping
        new_x_min, new_x_max = sorted([new_x_min, new_x_max])

        # Clamp values to image boundaries
        new_x_min = max(0, min(img_width, new_x_min))
        new_x_max = max(0, min(img_width, new_x_max))

        # print(f"Flipped bbox (pixels): {[new_x_min, y_min, new_x_max, y_max, class_id]}")

        return [new_x_min, y_min, new_x_max, y_max, class_id]

    def yolo_to_voc(self,bbox, img_width, img_height):
        class_id, x_center, y_center, width, height = bbox
        x_center *= img_width
        y_center *= img_height
        width *= img_width
        height *= img_height
        x_min = x_center - width / 2
        y_min = y_center - height / 2
        x_max = x_center + width / 2
        y_max = y_center + height / 2
        return [x_min, y_min, x_max, y_max, int(class_id)]

    def voc_to_yolo(bbox, img_width, img_height):
        x_min, y_min, x_max, y_max, class_id = bbox
        x_center = (x_min + x_max) / 2 / img_width
        y_center = (y_min + y_max) / 2 / img_height
        width = (x_max - x_min) / img_width
        height = (y_max - y_min) / img_height
        return [class_id, x_center, y_center, width, height]



    def transform_rotate_bbox(self, bbox, image_width, image_height, angle):
        """
        Rotates a bounding box around the center of the image and returns the new AABB (Axis-Aligned Bounding Box).

        Args:
            bbox: list of [x_min, y_min, x_max, y_max, class_id]
            angle: rotation angle in degrees (positive is counter-clockwise)
            image_width: width of the original image
            image_height: height of the original image

        Returns:
            list of [new_x_min, new_y_min, new_x_max, new_y_max, class_id]
        """
        x_min, y_min, x_max, y_max, class_id = bbox

        # Original corner points of the bounding box
        corners = np.array([
            [x_min, y_min],
            [x_min, y_max],
            [x_max, y_min],
            [x_max, y_max]
        ])

        # Center of the image
        center = (image_width / 2, image_height / 2)

        # Rotation matrix without translation adjustment
        M = cv2.getRotationMatrix2D(center, angle, 1.0)

        # Convert corners to homogeneous coordinates
        ones = np.ones((4, 1))
        corners_ones = np.hstack([corners, ones])

        # Rotate corners
        rotated_corners = M.dot(corners_ones.T).T

        # Get axis-aligned bounding box from rotated corners
        x_coords = rotated_corners[:, 0]
        y_coords = rotated_corners[:, 1]

        new_x_min = int(np.clip(np.min(x_coords), 0, image_width - 1))
        new_y_min = int(np.clip(np.min(y_coords), 0, image_height - 1))
        new_x_max = int(np.clip(np.max(x_coords), 0, image_width - 1))
        new_y_max = int(np.clip(np.max(y_coords), 0, image_height - 1))

        return [new_x_min, new_y_min, new_x_max, new_y_max, class_id]


    def transform_zoom_bbox(self, bbox, img_width, img_height, scale_factor):
        """Transform bounding box coordinates for zoom"""
        x_min, y_min, x_max, y_max, class_id = bbox

        # Image center
        cx, cy = img_width / 2, img_height / 2

        # Calculate new dimensions
        new_width = img_width / scale_factor
        new_height = img_height / scale_factor

        # Calculate offset
        left = (img_width - new_width) / 2
        top = (img_height - new_height) / 2

        # Transform coordinates
        new_x_min = (x_min - left) * scale_factor
        new_y_min = (y_min - top) * scale_factor
        new_x_max = (x_max - left) * scale_factor
        new_y_max = (y_max - top) * scale_factor

        # Clip to image boundaries
        new_x_min = max(0, min(img_width, new_x_min))
        new_y_min = max(0, min(img_height, new_y_min))
        new_x_max = max(0, min(img_width, new_x_max))
        new_y_max = max(0, min(img_height, new_y_max))

        return [new_x_min, new_y_min, new_x_max, new_y_max, class_id]

    # def apply_augmentations(self, image_path, save_dir, params, bboxes=None):
    #     """Apply augmentations to an image and save results"""
    #     # Read image
    #     image = cv2.imread(image_path)
    #     if image is None:
    #         print(f"Error: Could not read image {image_path}")
    #         return []

    #     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #     height, width = image.shape[:2]

    #     os.makedirs(save_dir, exist_ok=True)
    #     base_name = os.path.splitext(os.path.basename(image_path))[0]

    #     results = []

    #     for aug_name, active in params.items():
    #         if active and aug_name in self.augmentations:
    #             aug_config = self.augmentations[aug_name]
    #             value = params.get(f"{aug_name}_value", aug_config["default"])

    #             # Skip if this augmentation requires bboxes but we don't have any
    #             if aug_config["requires_bbox"] and not bboxes:
    #                 continue

    #             # Convert bboxes to numpy array if they exist
    #             bboxes_np = None
    #             if bboxes and aug_config["requires_bbox"]:
    #                 bboxes_np = np.array(bboxes, dtype=np.float32)
    #                 if bboxes_np.size == 0:
    #                     bboxes_np = None

    #             transform = aug_config["func"](value)

    #             try:
    #                 if aug_config["affects_bbox"] and bboxes:
    #                     # Apply transformation to image
    #                     transformed = transform(image=image)
    #                     transformed_image = transformed["image"]

    #                     # Apply custom bbox transformation
    #                     transformed_bboxes = []
    #                     for bbox in bboxes:
    #                         if aug_name == "flip":
    #                             new_bbox = aug_config["transform_bbox"](bbox, width, height)
    #                         elif aug_name == "rotate":
    #                             new_bbox = aug_config["transform_bbox"](bbox, width, height, value)
    #                         elif aug_name == "zoom":
    #                             scale_factor = 1 / ((value[0] + value[1]) / 2)  # Average scale factor
    #                             new_bbox = aug_config["transform_bbox"](bbox, width, height, scale_factor)

    #                         if self.is_valid_bbox(new_bbox, width, height):
    #                             transformed_bboxes.append(new_bbox)

    #                     # Save augmented image
    #                     aug_path = os.path.join(save_dir, f"{base_name}_{aug_name}.jpg")
    #                     cv2.imwrite(aug_path, cv2.cvtColor(transformed_image, cv2.COLOR_RGB2BGR))

    #                     # Save augmented bboxes if we have valid ones
    #                     if transformed_bboxes:
    #                         txt_path = os.path.join(save_dir, f"{base_name}_{aug_name}.txt")
    #                         self.save_yolo_annotations(txt_path, transformed_bboxes, width, height)
    #                         results.append((aug_path, txt_path))
    #                     else:
    #                         results.append((aug_path, None))
    #                 else:
    #                     # For transformations that don't affect bboxes
    #                     transformed = transform(image=image)['image']
    #                     aug_path = os.path.join(save_dir, f"{base_name}_{aug_name}.jpg")
    #                     cv2.imwrite(aug_path, cv2.cvtColor(transformed, cv2.COLOR_RGB2BGR))

    #                     # If original had annotations, copy them (unchanged)
    #                     txt_path = None
    #                     if bboxes:
    #                         orig_txt = os.path.splitext(image_path)[0] + ".txt"
    #                         new_txt = os.path.join(save_dir, f"{base_name}_{aug_name}.txt")
    #                         if os.path.exists(orig_txt):
    #                             import shutil
    #                             shutil.copy(orig_txt, new_txt)
    #                             txt_path = new_txt

    #                     results.append((aug_path, txt_path))
    #             except Exception as e:
    #                 print(f"Error applying {aug_name} to {image_path}: {str(e)}")
    #                 continue

    #     return results
    def apply_augmentations(self, image_path, save_dir, params, bboxes=None, formats=None, class_list=None):
        """Apply augmentations to an image and save results"""
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not read image {image_path}")
            return []

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width = image.shape[:2]

        os.makedirs(save_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(image_path))[0]

        results = []

        if formats is None:
            formats = {"yolo": True}
        if class_list is None:
            class_list = []

        for aug_name, active in params.items():
            if active and aug_name in self.augmentations:
                aug_config = self.augmentations[aug_name]
                value = params.get(f"{aug_name}_value", aug_config["default"])

                if aug_config["requires_bbox"] and not bboxes:
                    continue

                if aug_name == "zoom":
                    scale_range = value
                    min_val, max_val = scale_range
                    random_value = round(random.uniform(min_val, max_val), 1)
                    base_transform = [
                        A.RandomScale(scale_limit=(random_value - 1.0, random_value - 1.0), p=1.0),
                        A.PadIfNeeded(min_height=height, min_width=width, border_mode=cv2.BORDER_CONSTANT),
                        A.RandomCrop(height=height, width=width)
                    ]
                    if bboxes:
                        transform = A.Compose(base_transform,
                            bbox_params=A.BboxParams(format='pascal_voc', label_fields=['class_labels'], min_visibility=0.0)
                        )
                    else:
                        transform = A.Compose(base_transform)
                else:
                    transform = aug_config["func"](value)

                if aug_name == "rotate":
                    transform = aug_config["func"](value)
                    angle = self.last_sampled_angle

                try:
                    if aug_config["affects_bbox"] and bboxes:
                        if aug_name == "zoom":
                            transformed = transform(image=image, bboxes=bboxes, class_labels=['object'] * len(bboxes))
                            transformed_image = transformed["image"]
                            transformed_bboxes = transformed["bboxes"]
                        else:
                            transformed = transform(image=image)
                            transformed_image = transformed["image"]
                            transformed_bboxes = []
                            for bbox in bboxes:
                                if aug_name == "flip":
                                    new_bbox = aug_config["transform_bbox"](bbox, width, height)
                                elif aug_name == "rotate":
                                    new_bbox = aug_config["transform_bbox"](bbox, width, height, angle)
                                if self.is_valid_bbox(new_bbox, width, height):
                                    transformed_bboxes.append(new_bbox)

                    else:
                        # For transformations that don't affect bboxes
                        transformed = transform(image=image)
                        transformed_image = transformed["image"]
                        transformed_bboxes = bboxes if bboxes else []

                    # Save augmented image
                    aug_path = os.path.join(save_dir, f"{base_name}_{aug_name}.jpg")
                    cv2.imwrite(aug_path, cv2.cvtColor(transformed_image, cv2.COLOR_RGB2BGR))

                    txt_path = None
                    if transformed_bboxes and formats.get("yolo", True):
                        txt_path = os.path.join(save_dir, f"{base_name}_{aug_name}.txt")
                        self.save_yolo_annotations(txt_path, transformed_bboxes, width, height)

                    if transformed_bboxes and formats.get("json", False):
                        json_path = os.path.join(save_dir, f"{base_name}_{aug_name}.json")
                        with open(json_path, 'w') as jf:
                            json_data = []
                            for bbox in transformed_bboxes:
                                x_min, y_min, x_max, y_max, class_id = bbox
                                json_data.append({
                                    "class_id": class_id,
                                    "class_name": class_list[class_id] if class_id < len(class_list) else "unknown",
                                    "x1": x_min,
                                    "y1": y_min,
                                    "x2": x_max,
                                    "y2": y_max
                                })
                            json.dump(json_data, jf, indent=4)

                    if transformed_bboxes and formats.get("xml", False):
                        xml_path = os.path.join(save_dir, f"{base_name}_{aug_name}.xml")
                        root = ET.Element("annotation")
                        ET.SubElement(root, "filename").text = os.path.basename(aug_path)
                        size = ET.SubElement(root, "size")
                        ET.SubElement(size, "width").text = str(width)
                        ET.SubElement(size, "height").text = str(height)
                        ET.SubElement(size, "depth").text = "3"
                        for bbox in transformed_bboxes:
                            x_min, y_min, x_max, y_max, class_id = bbox
                            obj = ET.SubElement(root, "object")
                            ET.SubElement(obj, "name").text = class_list[class_id] if class_id < len(class_list) else "unknown"
                            bndbox = ET.SubElement(obj, "bndbox")
                            ET.SubElement(bndbox, "xmin").text = str(int(x_min))
                            ET.SubElement(bndbox, "ymin").text = str(int(y_min))
                            ET.SubElement(bndbox, "xmax").text = str(int(x_max))
                            ET.SubElement(bndbox, "ymax").text = str(int(y_max))
                        tree = ET.ElementTree(root)
                        tree.write(xml_path)

                    results.append((aug_path, txt_path))

                except Exception as e:
                    print(f"Error applying {aug_name} to {image_path}: {str(e)}")
                    continue

        return results



    def is_valid_bbox(self, bbox, img_width, img_height):
        """Check if a bounding box is valid"""
        if len(bbox) < 5:
            return False

        x_min, y_min, x_max, y_max, _ = bbox

        # Check if bbox is within image bounds and has positive area
        if x_min >= x_max or y_min >= y_max:
            return False
        if x_max <= 0 or x_min >= img_width:
            return False
        if y_max <= 0 or y_min >= img_height:
            return False

        # Check if bbox has reasonable size
        if (x_max - x_min) < 5 or (y_max - y_min) < 5:
            return False

        return True

    def read_yolo_annotations(self, annotation_path, img_width, img_height):
        """Read YOLO format annotations and convert to pixel coordinates"""
        bboxes = []
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

                        # Convert to pixel coordinates [x_min, y_min, x_max, y_max, class_id]
                        x_min = (x_center - width/2) * img_width
                        y_min = (y_center - height/2) * img_height
                        x_max = (x_center + width/2) * img_width
                        y_max = (y_center + height/2) * img_height

                        bboxes.append([x_min, y_min, x_max, y_max, class_id])
                # print(f"YOLO values: {parts} | Image dimensions: {img_width}x{img_height}")
        return bboxes

    def save_yolo_annotations(self, file_path, bboxes, img_width, img_height):
        """Save bounding boxes in YOLO format"""
        with open(file_path, 'w') as f:
            for bbox in bboxes:
                if len(bbox) < 5:
                    continue

                x_min, y_min, x_max, y_max, class_id = bbox

                # Convert to YOLO format [class_id, x_center, y_center, width, height]
                x_center = ((x_min + x_max) / 2) / img_width
                y_center = ((y_min + y_max) / 2) / img_height
                width = (x_max - x_min) / img_width
                height = (y_max - y_min) / img_height

                # Clip values to [0,1] range
                x_center = max(0, min(1, x_center))
                y_center = max(0, min(1, y_center))
                width = max(0, min(1, width))
                height = max(0, min(1, height))

                # Only save if the bbox is still valid
                if width > 0 and height > 0:
                    f.write(f"{int(class_id)} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")