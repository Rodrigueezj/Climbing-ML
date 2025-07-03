import os
import cv2
import pytesseract
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import cv2
import os

def is_benchmark(image, filename=None, debug=False, output_dir="debug_benchmark"):
    """
    Detects whether the benchmark 'B' icon is present in the header.
    If debug=True, saves visualization images to disk instead of showing them.

    Parameters:
    - image: input image (OpenCV format)
    - filename: original image filename, used to name debug files
    - debug: if True, saves debug images
    - output_dir: folder to save debug images
    """

    h, w, _ = image.shape
    y1, y2 = int(0 * h), int(0.33 * h)   # Title line area
    x1, x2 = int(0.4 * w), int(0.95 * w)   # Zone of the 'B' icon
    crop = image[y1:y2, x1:x2]

    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    lower_yellow = (20, 100, 100)
    upper_yellow = (35, 255, 255)
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    yellow_pixels = cv2.countNonZero(mask)

    if debug and filename:
        os.makedirs(output_dir, exist_ok=True)
        base = os.path.splitext(os.path.basename(filename))[0]

        # Original image with rectangle
        vis_img = image.copy()
        cv2.rectangle(vis_img, (x1, y1), (x2, y2), (0, 255, 255), 2)
        cv2.imwrite(os.path.join(output_dir, f"{base}_region.png"), vis_img)

        # Yellow mask
        cv2.imwrite(os.path.join(output_dir, f"{base}_mask.png"), mask)

    return yellow_pixels > 50

def count_stars(image, debug=False, filename=None, output_dir="debug_stars"):
    """
    Counts how many stars are filled with yellow.
    The region is divided into 5 horizontal sections, one for each star, and checks each one.

    Parameters:
    - image: the input image (BGR format)
    - debug: if True, saves debug images showing the mask and star sections
    - filename: the name of the image file (used for naming debug outputs)
    - output_dir: directory where debug images will be saved

    Returns:
    - star_count: number of detected filled (yellow) stars
    """

    h, w, _ = image.shape
    y1, y2 = int(0.80 * h), int(h)
    x1, x2 = int(0.38 * w), int(0.624 * w)
    crop = image[y1:y2, x1:x2]

    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    lower_yellow = (20, 100, 100)
    upper_yellow = (35, 255, 255)
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Dividing the mask into 5 sections
    # Each section corresponds to a star
    section_width = mask.shape[1] // 5
    star_count = 0
    threshold = 200  # min yellow pixels to consider a star filled

    for i in range(5):
        x_start = i * section_width
        x_end = (i + 1) * section_width
        section = mask[:, x_start:x_end]
        yellow_pixels = cv2.countNonZero(section)
        if yellow_pixels > threshold:
            star_count += 1

    if debug and filename:
        os.makedirs(output_dir, exist_ok=True)
        base = os.path.splitext(os.path.basename(filename))[0]
        debug_path_mask = os.path.join(output_dir, f"{base}_stars_mask.png")
        debug_path_overlay = os.path.join(output_dir, f"{base}_stars_overlay.png")

        # save the mask image
        cv2.imwrite(debug_path_mask, mask)

        # Draw vertical lines to visualize sections
        debug_img = crop.copy()
        for i in range(1, 5):
            x = i * section_width
            cv2.line(debug_img, (x, 0), (x, debug_img.shape[0]), (255, 0, 0), 1)
        cv2.imwrite(debug_path_overlay, debug_img)

    return star_count

def process_image_ocr(image_path):
    """
    Reads an image from the given path and applies OCR to extract:
    - Route name
    - Grade

    Returns a dictionary with the extracted fields or None if the image is invalid.

    Parameters:
    - image_path: path to the image file

    Returns:
    - A dictionary with:
        - 'filename': the image file name
        - 'grade': the extracted grade (or "unknown" if not found)
        - 'benchmark': whether the route is marked as benchmark
        - 'stars': number of yellow-filled stars
    """

    image = cv2.imread(image_path)
    if image is None:
        return None  # Image could not be read

    # Apply OCR to the image
    text = pytesseract.image_to_string(image)

    # Cleaning empty lines and stripping whitespace
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    # Safely extract the name and grade
    grade = lines[2] if len(lines) > 2 else "unknown"

    filename = os.path.basename(image_path)

    benchmark = is_benchmark(image, filename=image_path, debug=False)
    stars = count_stars(image, debug=False, filename=image_path)

    return {
        "filename": filename,
        "grade": grade,
        "benchmark": True if benchmark else False,
        "stars": stars,
    }

# Principal function to extract metadata from header images

def extract_metadata(header_dir):
    """
    Iterates through all header images in the given directory (`header_dir`),
    applies OCR in parallel using multithreading, and builds a DataFrame with the results.

    Returns:
    - pandas.DataFrame with the following columns:
        - filename: image filename
        - name: extracted route name (if applicable)
        - grade: extracted grade
        - stars: number of yellow-filled stars
        - mark: benchmark flag
    """

    # Get all PNG image paths in the header directory
    image_paths = [
        os.path.join(header_dir, f)
        for f in os.listdir(header_dir)
        if f.lower().endswith(".png")
    ]

    print(f"🔎 Processing {len(image_paths)} headers with OCR in parallel...")

    results = []

    # Create a ThreadPoolExecutor to process images in parallel
    with ThreadPoolExecutor() as executor:
        # Send each image path to the executor
        futures = [executor.submit(process_image_ocr, path) for path in image_paths]

        # Using tqdm to show progress
        for future in tqdm(as_completed(futures), total=len(futures), desc="OCR"):
            result = future.result()
            if result:
                results.append(result)

    print("✅ OCR Completed.")
    return pd.DataFrame(results)
