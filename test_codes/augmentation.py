import cv2
import albumentations as A
import numpy as np
import os

def apply_augmentations(image_path, save_dir, params):
    """
    Apply various augmentations to an image and save the results.
    :param image_path: Path to the input image.
    :param save_dir: Directory to save the augmented images.
    :param params: Dictionary containing augmentation parameters.
    """
    # Load image
    image = cv2.imread(image_path)
    height, width = image.shape[:2]

    # Ensure save directory exists
    os.makedirs(save_dir, exist_ok=True)

    augmentations = {
        "flip": A.HorizontalFlip(p=1) if params.get("flip", False) else None,
        "rotate": A.Rotate(limit=params.get("rotate", 30), p=1),
        "crop": A.RandomCrop(height=height//2, width=width//2, p=1),
        "blur": A.GaussianBlur(blur_limit=params.get("blur", (3, 7)), p=1),
        "noise": A.GaussNoise(var_limit=params.get("noise", (10.0, 50.0)), p=1),
        "zoom": A.RandomScale(scale_limit=params.get("zoom", (0.8, 1.2)), p=1),
        "brightness": A.RandomBrightnessContrast(
            brightness_limit=params.get("brightness", 0.2),
            contrast_limit=params.get("contrast", 0.2), p=1
        ),
        "hue_saturation": A.HueSaturationValue(
            hue_shift_limit=params.get("hue", 20),
            sat_shift_limit=params.get("saturation", 30), p=1
        )
    }

    for name, aug in augmentations.items():
        if aug is not None:
            transformed = aug(image=image)['image']
            transformed = cv2.resize(transformed, (width, height))  # Keep original dimensions
            cv2.imwrite(os.path.join(save_dir, f"{name}.jpg"), transformed)

    print(f"Augmented images saved in {save_dir}")

# Example usage
image_path = "images/20250110_151058.jpg"  # Change to your image path
save_directory = "augmented_images"

# Define parameter values with acceptable ranges
params = {
    "flip": True,  # Flip image
    "rotate": 45,  # Range: -90 to 90
    "blur": (5, 5),  # Kernel size range (odd numbers only)
    "noise": (10.0, 50.0),  # Variance range
    "zoom": (0.8, 1.2),  # Scale range (0.5 to 1.5 recommended)
    "brightness": 0.3,  # Range: 0 to 1
    "contrast": 0.3,  # Range: 0 to 1
    "hue": 20,  # Range: -30 to 30
    "saturation": 30  # Range: -50 to 50
}

apply_augmentations(image_path, save_directory, params)
