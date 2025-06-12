import os
import time
import config

# Folder where images will be saved
SAVE_DIR = config.RAW_DIR
os.makedirs(SAVE_DIR, exist_ok=True)

# Number of captures to perform
NUM_CAPTURES = 50000

# Swipe coordinates
# swipe: from (x1, y1) to (x2, y2)
SWIPE_X1, SWIPE_Y1 = 900, 800
SWIPE_X2, SWIPE_Y2 = 200, 800
SWIPE_DURATION_MS = 10 # duration in miliseconds

def capture_and_pull(i):
    # Screencap on the device
    os.system("adb shell screencap -p /sdcard/screen.png")
    
    # Download the image to the local machine
    local_path = os.path.join(SAVE_DIR, f"moonboard_{i:04}.png")
    os.system(f"adb pull /sdcard/screen.png {local_path}")
    print(f"[✓] Imagen guardada: {local_path}")

def swipe_left():
    os.system(f"adb shell input swipe {SWIPE_X1} {SWIPE_Y1} {SWIPE_X2} {SWIPE_Y2} {SWIPE_DURATION_MS}")

def main():
    for i in range(1, NUM_CAPTURES + 1):
        print(f"[{i}] Capturando ruta...")
        capture_and_pull(i)
        time.sleep(0.0001)  # Wait for the image to be saved
        swipe_left()
        time.sleep(0.0001)  # Wait for the swipe to complete

if __name__ == "__main__":
    main()
