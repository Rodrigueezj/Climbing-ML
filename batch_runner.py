import os
import shutil
from glob import glob
from pathlib import Path
from math import ceil

from moonboard.parallel_header_cropper import crop_header
from moonboard.ocr_parallel_extractor import extract_metadata
from moonboard.parallel_board_cropper import crop_boards
import moonboard.config as config
import pandas as pd

def split_into_batches(input_dir, batch_size, output_base):
    """
    Splits the .png files in input_dir into subfolders of size batch_size.
    """
    all_images = sorted(glob(os.path.join(input_dir, "*.png")))
    total_batches = ceil(len(all_images) / batch_size)
    print(f"📦 Splitting {len(all_images)} images into {total_batches} batches...")

    Path(output_base).mkdir(parents=True, exist_ok=True)

    for i in range(total_batches):
        batch_dir = os.path.join(output_base, f"batch_{i+1:03d}")
        Path(batch_dir).mkdir(exist_ok=True)

        batch_images = all_images[i * batch_size : (i + 1) * batch_size]
        for img in batch_images:
            shutil.copy(img, batch_dir)

    print("✅ Split completed.")

def run_batch(batch_name, raw_dir, headers_dir, boards_dir, metadata_csv, header_coords, board_coords):
    """
    Runs the full pipeline on a single batch.
    """
    print(f"\n🚀 Running batch: {batch_name}")

    # Step 1: Header crop
    crop_header(
        input_dir=raw_dir,
        output_dir=headers_dir,
        coords=header_coords
    )

    # Step 2: OCR
    df = extract_metadata(headers_dir)
    df.to_csv(metadata_csv, index=False)
    print(f"📄 Metadata saved to {metadata_csv}")

    # Step 3: Board crop
    crop_boards(
        screenshot_dir=raw_dir,
        metadata_csv=metadata_csv,
        output_dir=boards_dir,
        coords=board_coords
    )

    print(f"🎉 Batch {batch_name} complete.")

def main():
    batch_size = 1000
    original_screenshots = config.RAW_DIR3
    batches_dir = "batches"
    start_from = 37  # Batch desde el cual quieres continuar


    # Step 0: Split into batches if not already done
    if not os.path.exists(batches_dir):
        split_into_batches(original_screenshots, batch_size, batches_dir)

    batch_folders = sorted(os.listdir(batches_dir))
    for i, batch_name in enumerate(batch_folders):
        if i + 1 < start_from:
            continue  # Skip previous batches

        batch_raw_dir = os.path.join(batches_dir, batch_name)
        headers_dir = os.path.join("headers", batch_name)
        boards_dir = os.path.join("boards", batch_name)
        metadata_csv = os.path.join("metadata", f"{batch_name}.csv")

        Path(headers_dir).mkdir(parents=True, exist_ok=True)
        Path(boards_dir).mkdir(parents=True, exist_ok=True)
        Path("metadata").mkdir(exist_ok=True)

        run_batch(
            batch_name=batch_name,
            raw_dir=batch_raw_dir,
            headers_dir=headers_dir,
            boards_dir=boards_dir,
            metadata_csv=metadata_csv,
            header_coords=config.HEADER_COORDS,
            board_coords=config.BOARD_COORDS
        )

if __name__ == "__main__":
    main()
