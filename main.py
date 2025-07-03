from data_preprocessing.parallel_cropper import crop_header
from data_preprocessing.ocr_parallel_extractor import extract_metadata
from data_preprocessing.build_dataframe import build_csv
from data_preprocessing.image_to_matrix import image_to_matrix

import data_preprocessing.config as config

def main():

    print("📦 Paso 1: Header cropping...")
    crop_header(
        input_dir=config.RAW_DIR,
        output_dir=config.HEADERS_DIR,
        coords=config.HEADER_COORDS
    )

    print("🎯 Paso 2: Board cropping...")
    crop_header(
        input_dir=config.RAW_DIR,
        output_dir=config.BOARDS_DIR,
        coords=config.BOARD_COORDS
    )

    print("🔎 Paso 3: Extracting metadata from headers...")
    df = extract_metadata(config.HEADERS_DIR)
    df.to_csv(config.METADATA_CSV, index=False)
    print(f"✅ Metadata saved in: {config.METADATA_CSV}")

    #Dataframe with matrices
    build_csv(
    image_dir="./data/moonboards",
    metadata_csv="metadata.csv",
    image_to_matrix_func=image_to_matrix,
    output_csv="final_data.csv"
)

    print("🎉 Pipeline completed successfully.")

if __name__ == "__main__":
    main()