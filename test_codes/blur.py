# import cv2
# import numpy as np
# import os

# def apply_opencv_blur_and_compare(image_path, save_dir):
#     image = cv2.imread(image_path)
#     if image is None:
#         print("Error loading image")
#         return

#     os.makedirs(save_dir, exist_ok=True)

#     # Apply OpenCV Gaussian Blur directly (strong visible blur)
#     blurred = cv2.GaussianBlur(image, (35, 35), sigmaX=5)

#     # Add text to both images
#     original = image.copy()
#     cv2.putText(original, "Original", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
#     cv2.putText(blurred, "Blurred", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

#     # Save individually
#     cv2.imwrite(os.path.join(save_dir, "original.jpg"), original)
#     cv2.imwrite(os.path.join(save_dir, "blurred.jpg"), blurred)

#     # Side-by-side comparison
#     side_by_side = np.hstack((original, blurred))
#     cv2.imwrite(os.path.join(save_dir, "opencv_blur_comparison.jpg"), side_by_side)
#     print("Saved OpenCV-based blurred comparison.")

# # Usage
# apply_opencv_blur_and_compare("images/sam_combined (140).jpg", "opencv_blur_output")

# import cv2
# import albumentations as A
# import numpy as np
# import os

# def apply_gaussian_blur_and_compare(image_path, save_dir):
#     """
#     Applies a strong Gaussian blur using Albumentations and compares the original and blurred image.
#     Saves both separately and a side-by-side comparison.
#     """
#     # Load original image
#     image = cv2.imread(image_path)
#     if image is None:
#         print(f"Error loading image: {image_path}")
#         return

#     # Ensure save directory exists
#     os.makedirs(save_dir, exist_ok=True)

#     height, width = image.shape[:2]

#     # Strong Albumentations Gaussian Blur
#     blur_aug = A.GaussianBlur(
#         blur_limit=0,                   # Let Albumentations compute kernel from sigma
#         sigma_limit=(5.0, 7.0),         # Very strong blur
#         p=1.0                           # Always apply
#     )

#     # Apply the transformation
#     transformed = blur_aug(image=image)["image"]

#     # Add overlay text
#     labeled_original = image.copy()
#     labeled_blurred = transformed.copy()
#     cv2.putText(labeled_original, "Original", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
#                 1, (0, 0, 255), 2, cv2.LINE_AA)
#     cv2.putText(labeled_blurred, "Blurred", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
#                 1, (255, 0, 0), 2, cv2.LINE_AA)

#     # Save individually
#     cv2.imwrite(os.path.join(save_dir, "original.jpg"), labeled_original)
#     cv2.imwrite(os.path.join(save_dir, "blurred.jpg"), labeled_blurred)

#     # Side-by-side comparison
#     side_by_side = np.hstack((labeled_original, labeled_blurred))
#     cv2.imwrite(os.path.join(save_dir, "albumentations_strong_blur.jpg"), side_by_side)
#     print("Saved images in:", save_dir)

# # --------- Example Usage ---------
# image_path = "images/20250110_151058.jpg"  # Update with your actual path
# save_directory = "albumentations_blur_output"

# apply_gaussian_blur_and_compare(image_path, save_directory)

import cv2
import albumentations as A
import numpy as np
import os

def apply_multiple_blur_levels(image_path, save_dir, sigma_values=(0.5, 2.0, 4.0, 6.0, 7.0, 10.0)):
    """
    Apply multiple levels of Gaussian blur to visualize from low to heavy blur.
    Saves each level and a side-by-side composite.
    """
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error loading image: {image_path}")
        return

    os.makedirs(save_dir, exist_ok=True)
    blurred_images = []

    # Add original for comparison
    labeled_original = image.copy()
    cv2.putText(labeled_original, "Original", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2, cv2.LINE_AA)
    blurred_images.append(labeled_original)

    for sigma in sigma_values:
        # Apply blur with fixed sigma
        blur_aug = A.GaussianBlur(blur_limit=0, sigma_limit=(sigma, sigma), p=1.0)
        transformed = blur_aug(image=image)["image"]

        labeled_blurred = transformed.copy()
        cv2.putText(labeled_blurred, f"Sigma {sigma}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 0, 0), 2, cv2.LINE_AA)
        blurred_images.append(labeled_blurred)

        # Save individual blurred image
        cv2.imwrite(os.path.join(save_dir, f"blur_sigma_{sigma}.jpg"), labeled_blurred)

    # Save side-by-side composite
    combined = np.hstack(blurred_images)
    cv2.imwrite(os.path.join(save_dir, "multi_blur_comparison.jpg"), combined)
    print(f"Saved blurred variations and comparison in '{save_dir}'")

# Example usage
image_path = "images/sam_combined (140).jpg"  # Update with your actual path
save_directory = "multi_blur_output"

apply_multiple_blur_levels(image_path, save_directory)
