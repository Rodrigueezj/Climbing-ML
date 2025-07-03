# During the exploration phase, I realized I did not take into account the emojis that users can place in the route names.
# I was deciding whether a rout name was a benchmark or not based on the amount of yellow pixels in the header.
# Now I will use a more robust method that checks for the presence of the 'B' icon in the header.

import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm
import os

import cv2
import os

def crop_benchmark_template(image_path, output_path, coords):
    """
    Crops the region where the yellow benchmark 'B' is located and saves it as an image.

    Parameters:
    - image_path: path to the image from which the 'B' will be cropped.
    - output_path: path to save the cropped template image.
    - coords: tuple (y1, y2, x1, x2) defining the crop area.
    """
    
    img = cv2.imread(image_path)
    if img is None:
        print(f"⚠️ Image could not be read: {image_path}")
        return

    y1, y2, x1, x2 = coords
    cropped = img[y1:y2, x1:x2]
    cv2.imwrite(output_path, cropped)
    print(f"✅ Template saved in: {output_path}")

def detect_benchmark_b(image_path, template_path, threshold=0.8, debug=False, debug_output_dir="debug_benchmark"):
    """
    Detects whether an image contains the yellow benchmark 'B' using template matching.

    Parameters:
    - image_path: path to the input image.
    - template_path: path to the cropped yellow 'B' template.
    - threshold: minimum correlation value to accept a match (default is 0.8).
    - debug: if True, saves the image with the matched region highlighted.
    - debug_output_dir: directory to save debug images if debug is enabled.

    Returns:
    - True if the benchmark 'B' is detected, False otherwise.
    """

    image = cv2.imread(image_path)
    template = cv2.imread(template_path)
    if image is None or template is None:
        print(f"⚠️ The image or template couldn't be loaded: {image_path}")
        return False

    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_img, gray_template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        if debug:
            os.makedirs(debug_output_dir, exist_ok=True)
            h, w = gray_template.shape
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
            debug_path = os.path.join(debug_output_dir, os.path.basename(image_path))
            cv2.imwrite(debug_path, image)
        return True
    else:
        return False
    
df = pd.read_csv("final_data.csv")

# Loading the benchmark template
template = "template_benchmark.png"

# Routes to the images
image_dir = "data/headers/" 

# Processing and adding the benchmark column
benchmark_flags = []
for filename in tqdm(df["filename"], desc="Detectando benchmark"):
    image_path = os.path.join(image_dir, filename)
    is_benchmark = detect_benchmark_b(image_path, template)
    benchmark_flags.append(is_benchmark)

df["benchmark"] = benchmark_flags

# Saves the new CSV
df.to_csv("final_data_with_benchmark.csv", index=False)
print("✅ Nueva columna 'benchmark' añadida y guardada en final_data_with_benchmark.csv")