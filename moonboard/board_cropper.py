import os
import cv2
import pandas as pd
import re


def crop_boards(screenshot_dir, metadata_csv, output_dir, coords):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(metadata_csv)

    y1, y2, x1, x2 = coords

    for _, row in df.iterrows():
        filename = row["filename"]
        name = row["name"]
        safe_name = re.sub(r'\W+', '_', name)[:100]

        input_path = os.path.join(screenshot_dir, filename)
        output_path = os.path.join(output_dir, f"{safe_name}.png")

        img = cv2.imread(input_path)
        if img is None:
            print(f"❌ Unable to load {filename}")
            continue

        board = img[y1:y2, x1:x2]
        cv2.imwrite(output_path, board)

    print(f"✅ {len(df)} Boards cropped in '{output_dir}'")
