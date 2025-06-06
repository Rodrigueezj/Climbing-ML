import os
import cv2
import pandas as pd
import re
from tqdm import tqdm

def crop_boards(screenshot_dir, metadata_csv, output_dir, coords):
    """
    Crop the MoonBoard area from the original screenshots using metadata extracted via OCR.

    Parameters:
    - screenshot_dir: path to the folder containing raw screenshots (.png)
    - metadata_csv: path to the CSV file with route metadata (name, filename, etc.)
    - output_dir: path to save cropped board images
    - coords: tuple (y1, y2, x1, x2) indicating the crop area
    """
    os.makedirs(output_dir, exist_ok=True)

    # Load metadata containing route names and original filenames
    df = pd.read_csv(metadata_csv)
    y1, y2, x1, x2 = coords

    print(f"📐 Cropping MoonBoard from {len(df)} screenshots...")

    # Iterate over each row in the metadata DataFrame
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Board Crop"):
        filename = row["filename"]
        route_name = row["name"]

        # Load the corresponding image
        image_path = os.path.join(screenshot_dir, filename)
        image = cv2.imread(image_path)

        if image is None:
            print(f"⚠️ Could not load image: {filename}")
            continue

        # Crop the board area using the provided coordinates
        board_crop = image[y1:y2, x1:x2]

        # Clean and shorten the route name to use as filename
        safe_name = re.sub(r'\W+', '_', route_name)[:100]
        output_path = os.path.join(output_dir, f"{safe_name}.png")

        # Save the cropped board image
        cv2.imwrite(output_path, board_crop)

    print(f"✅ Cropped boards saved in: {output_dir}")
