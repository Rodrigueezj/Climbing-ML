import os
import pandas as pd
import numpy as np
from tqdm import tqdm

def build_csv(image_dir, metadata_csv, image_to_matrix_func, output_csv):
    """
    Process images from the directory, applies `image_to_matrix_func`,
    And save them in a new csv with columns: filename, grade, matrix (como string), benchmark, stars.
    """

    metadata = pd.read_csv(metadata_csv)
    data = []

    for _, row in tqdm(metadata.iterrows(), total=len(metadata)):
        filename = row['filename']
        grade = row['grade']
        benchmark_val = row.get('benchmark')
        stars_val = row.get('stars')
        image_path = os.path.join(image_dir, filename)

        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            continue
        
        try:
            matrix = image_to_matrix_func(image_path)
            if matrix.shape != (18, 11):
                print(f"⚠️ {filename} returned a matrix of shape {matrix.shape}")
                raise ValueError(f"Invalid matrix for {filename}")
            matrix_str = matrix.astype(int).tolist()  # Save as list for better readability
            data.append({
                "filename": filename,
                "grade": grade,
                "matrix": matrix_str,
                "benchmark": benchmark_val,
                "stars": stars_val
            })

        except Exception as e:
            print(f"⚠️ Error con {filename}: {e}")
    
    # Convert to Dataframe and save to CSV
    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    print(f"✅ CSV guardado en: {output_csv}")