import os
import cv2
from tqdm import tqdm

def crop_header(input_dir, output_dir, coords):
    """
    Crop the top header area from each screenshot where route metadata is displayed.
    This includes route name, grade, stars, and marking.

    Parameters:
    - input_dir: folder containing the original full screenshots
    - output_dir: folder to store cropped header images
    - coords: tuple (y1, y2, x1, x2) defining the crop region
    """
    os.makedirs(output_dir, exist_ok=True)
    y1, y2, x1, x2 = coords

    # List all .png files in the input directory
    image_files = [
        f for f in os.listdir(input_dir)
        if f.lower().endswith(".png")
    ]

    print(f"📋 Cropping headers from {len(image_files)} screenshots...")

    # Loop through all image files with a progress bar
    for filename in tqdm(image_files, desc="Header Crop"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        # Load image
        image = cv2.imread(input_path)
        if image is None:
            print(f"⚠️ Could not load image: {filename}")
            continue

        # Crop the header section
        cropped = image[y1:y2, x1:x2]

        # Save the cropped header image
        cv2.imwrite(output_path, cropped)

    print(f"✅ Headers saved in: {output_dir}")