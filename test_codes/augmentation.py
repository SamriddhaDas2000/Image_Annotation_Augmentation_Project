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

    # Blur logic with blur_limit and sigma_limit
    blur_range = params.get("blur_limit", (3, 21))
    sigma_range = params.get("sigma_limit", (0.5, 3.0))

    blur_aug = A.GaussianBlur(
        blur_limit=blur_range,
        sigma_limit=sigma_range,
        p=1.0
    )

    # Define all augmentations
    augmentations = {
        "flip": A.HorizontalFlip(p=1) if params.get("flip", False) else None,
        "rotate": A.Rotate(limit=params.get("rotate", 30), p=1),
        "crop": A.RandomCrop(height=height//2, width=width//2, p=1),
        "blur": blur_aug,
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

    # Apply and save each augmentation
    for name, aug in augmentations.items():
        if aug is not None:
            transformed = aug(image=image)['image']
            transformed = cv2.resize(transformed, (width, height))  # Keep original dimensions
            cv2.imwrite(os.path.join(save_dir, f"{name}.jpg"), transformed)

    print(f"Augmented images saved in {save_dir}")

# Example usage
image_path = "images/sam_combined (140).jpg"  # Change to your image path
save_directory = "augment"

params = {
    "flip": True,
    "rotate": 45,
    "blur_limit": (9, 21),         # Kernel size range (odd numbers only)
    "sigma_limit": (1.0, 3.0),     # Standard deviation range
    "noise": (10.0, 50.0),
    "zoom": (0.8, 1.2),
    "brightness": 0.3,
    "contrast": 0.3,
    "hue": 20,
    "saturation": 30
}

apply_augmentations(image_path, save_directory, params)
