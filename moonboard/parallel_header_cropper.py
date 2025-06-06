import os
import cv2
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def crop_single_header(input_path, output_path, coords):
    """
    Helper function to crop one header image.
    """
    image = cv2.imread(input_path)
    if image is None:
        print(f"⚠️ Could not load image: {os.path.basename(input_path)}")
        return

    y1, y2, x1, x2 = coords
    cropped = image[y1:y2, x1:x2]
    cv2.imwrite(output_path, cropped)

def crop_header(input_dir, output_dir, coords):
    """
    Crop the top header from all images in input_dir and save to output_dir, using parallel threads.
    
    Parameters:
    - input_dir: directory with original screenshots
    - output_dir: directory to save cropped headers
    - coords: tuple (y1, y2, x1, x2) defining the crop rectangle
    """
    os.makedirs(output_dir, exist_ok=True)

    image_files = [
        f for f in os.listdir(input_dir)
        if f.lower().endswith(".png")
    ]

    print(f"📋 Cropping {len(image_files)} headers in parallel...")

    with ThreadPoolExecutor() as executor:
        futures = []
        for filename in image_files:
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            futures.append(executor.submit(crop_single_header, input_path, output_path, coords))

        for _ in tqdm(as_completed(futures), total=len(futures), desc="Header Crop"):
            pass

    print(f"✅ Cropped headers saved in: {output_dir}")