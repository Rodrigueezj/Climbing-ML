import cv2
import os

def crop_header(input_dir, output_dir, coords):
    os.makedirs(output_dir, exist_ok=True)
    
    y1, y2, x1, x2 = coords
    for filename in sorted(os.listdir(input_dir)):
        if not filename.lower().endswith(".png"):
            continue

        # Cargar imagen original
        img_path = os.path.join(input_dir, filename)
        img = cv2.imread(img_path)

        # Validar que se cargó bien
        if img is None:
            print(f"❌ No se pudo cargar {filename}")
            continue

        # Recortar la parte superior
        crop = img[y1:y2, x1:x2]

        # Guardar en routes/ con el mismo nombre
        cv2.imwrite(os.path.join(output_dir, filename), crop)