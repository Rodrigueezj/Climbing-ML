from moonboard.header_cropper import crop_header
from moonboard.ocr_extractor import extract_metadata
from moonboard.board_cropper import crop_boards
import moonboard.config as config
import pandas as pd


def main():

    print("📦 Paso 1: Recorte de encabezados...")
    crop_header(
        input_dir=config.RAW_TEST_DIR,
        output_dir=config.HEADERS_DIR,
        coords=config.HEADER_COORDS
    )

    print("🔎 Paso 2: OCR de encabezados...")
    df = extract_metadata(config.HEADERS_DIR)
    df.to_csv(config.METADATA_CSV, index=False)
    print(f"✅ Metadata guardada en: {config.METADATA_CSV}")

    print("🎯 Paso 3: Recorte del tablero completo...")
    crop_boards(
        screenshot_dir=config.RAW_TEST_DIR,
        metadata_csv=config.METADATA_CSV,
        output_dir=config.BOARDS_DIR,
        coords=config.BOARD_COORDS
    )

    print("🎉 Pipeline completado exitosamente.")

if __name__ == "__main__":
    main()