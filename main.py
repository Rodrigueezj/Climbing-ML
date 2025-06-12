from glob import glob
from pathlib import Path
from math import ceil

from data_preprocessing.parallel_cropper import crop_header
from data_preprocessing.ocr_parallel_extractor import extract_metadata
import data_preprocessing.config as config

def main():

    # print("📦 Paso 1: Recorte de encabezados...")
    # crop_header(
    #     input_dir=config.RAW_DIR,
    #     output_dir=config.HEADERS_DIR,
    #     coords=config.HEADER_COORDS
    # )

    # print("🎯 Paso 2: Recorte del tablero completo...")
    # crop_header(
    #     input_dir=config.RAW_DIR,
    #     output_dir=config.BOARDS_DIR,
    #     coords=config.BOARD_COORDS
    # )

    # print("🔎 Paso 3: OCR de encabezados...")
    # df = extract_metadata(config.HEADERS_DIR)
    # df.to_csv(config.METADATA_CSV, index=False)
    # print(f"✅ Metadata guardada en: {config.METADATA_CSV}")

    print("🎉 Pipeline completado exitosamente.")

if __name__ == "__main__":
    main()