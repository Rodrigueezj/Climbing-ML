import os
import cv2
import pandas as pd
import re
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def crop_single_board(screenshot_path, output_path, coords):
    """
    Crop the board area from a single screenshot and save it.
    """
    image = cv2.imread(screenshot_path)
    if image is None:
        print(f"⚠️ Could not load image: {os.path.basename(screenshot_path)}")
        return

    y1, y2, x1, x2 = coords
    cropped = image[y1:y2, x1:x2]
    cv2.imwrite(output_path, cropped)

def crop_boards(screenshot_dir, metadata_csv, output_dir, coords):
    """
    Crop the MoonBoard area from all screenshots using metadata, in parallel.
    
    Parameters:
    - screenshot_dir: folder containing raw screenshots
    - metadata_csv: path to metadata file with route names
    - output_dir: folder to save cropped board images
    - coords: tuple (y1, y2, x1, x2) defining crop region
    """
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(metadata_csv)
    y1, y2, x1, x2 = coords

    print(f"📐 Cropping boards from {len(df)} screenshots in parallel...")

    futures = []
    with ThreadPoolExecutor() as executor:
        for _, row in df.iterrows():
            filename = row["filename"]
            route_name = row["name"]

            # Clean the route name to use as filename
            safe_name = re.sub(r'\W+', '_', str(route_name))[:100]
            screenshot_path = os.path.join(screenshot_dir, filename)
            output_path = os.path.join(output_dir, f"{safe_name}.png")

            # Submit parallel job
            futures.append(executor.submit(crop_single_board, screenshot_path, output_path, coords))

        # Wait with progress bar
        for _ in tqdm(as_completed(futures), total=len(futures), desc="Board Crop"):
            pass

    print(f"✅ Cropped boards saved in: {output_dir}")
