import cv2
import numpy as np
import pandas as pd

import cv2
import numpy as np
import os

def image_to_matrix(image_path, debug_path=None):
    """
    Detects green, blue, and red circles in a cropped image of the MoonBoard
    and maps them to coordinates in an 18x11 matrix, generating a binary multi-channel matrix:
    - Channel 0: isHold (1 if there's a hold)
    - Channel 1: isStart (1 if it's a start hold)
    - Channel 2: isEnd (1 if it's a top hold)

    Parameters:
    - image_path: path to the input image
    - debug_path: if specified, saves a debug image with detections over the grid

    Returns:
    - matrix (numpy array of shape [18, 11, 3])
    """
    
    # Read Image
    img = cv2.imread(image_path)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    height, width = img.shape[:2]
    cell_h, cell_w = height // 18, width // 11

    # HSV range for colors(in OpenCV: H: 0-179, S,V: 0-255)
    ranges = {
        "green": ([50, 100, 100], [85, 255, 255]),
        "blue":  ([100, 100, 100], [130, 255, 255]),
        "red1":  ([0, 100, 100], [10, 255, 255]),
        "red2":  ([160, 100, 100], [180, 255, 255])
    }

    # Masks
    masks = {}
    for key, (lower, upper) in ranges.items():
        masks[key] = cv2.inRange(img_hsv, np.array(lower), np.array(upper))

    # Combining red masks
    masks["red"] = cv2.bitwise_or(masks["red1"], masks["red2"])

    # Matrix Initialization
    matrix = np.zeros((18, 11), dtype=np.uint8)

    # Center detection
    for idx, (color, mask) in enumerate([("green", masks["green"]), ("blue", masks["blue"]), ("red", masks["red"])]):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            M = cv2.moments(cnt)
            if M["m00"] == 0:
                continue
            cx, cy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
            row, col = cy // cell_h, cx // cell_w
            if 0 <= row < 18 and 0 <= col < 11:
                matrix[row, col] = 1  # isHold
                # if color == "green":
                #     matrix[row, col, 1] = 1  # isStart
                # elif color == "red":
                #     matrix[row, col, 2] = 1  # isEnd

    # Debug
    if debug_path:
        debug_img = img.copy()
        for r in range(1, 18):
            cv2.line(debug_img, (0, r * cell_h), (width, r * cell_h), (255, 255, 0), 1)
        for c in range(1, 11):
            cv2.line(debug_img, (c * cell_w, 0), (c * cell_w, height), (255, 255, 0), 1)
        for row in range(18):
            for col in range(11):
                if matrix[row, col, 1]:
                    color = (0, 255, 0)
                elif matrix[row, col, 2]:
                    color = (0, 0, 255)
                elif matrix[row, col, 0]:
                    color = (255, 0, 0)
                else:
                    continue
                center = (int((col + 0.5) * cell_w), int((row + 0.5) * cell_h))
                cv2.circle(debug_img, center, 10, color, 2)
        os.makedirs(os.path.dirname(debug_path), exist_ok=True)
        cv2.imwrite(debug_path, debug_img)

    return matrix