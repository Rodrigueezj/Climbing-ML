# config.py

# Coordinates (Y1, Y2, X1, X2)
HEADER_COORDS = (175, 300, 500, 1100)
BOARD_COORDS = (460, 2260, 290, 1390)
#BOARD_COORDS = (450, 2270, 537, 637)

# Base directory
BASE_IMAGE_DIR = "data"

# Subfolders
RAW_DIR     = f"{BASE_IMAGE_DIR}/raw"
RAW_TEST_DIR = f"{BASE_IMAGE_DIR}/raw_test"

# Output directories
HEADERS_DIR = f"{BASE_IMAGE_DIR}/headers"
HEADERS_TEST_DIR = f"{BASE_IMAGE_DIR}/headers_test"
BOARDS_DIR  = f"{BASE_IMAGE_DIR}/moonboards"

# Metadata CSV file
METADATA_CSV = "metadata.csv"