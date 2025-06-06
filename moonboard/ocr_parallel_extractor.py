import os
import cv2
import pytesseract
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Función auxiliar

def process_image_ocr(image_path):
    """
    Lee una imagen desde la ruta dada y aplica OCR para extraer:
    - Nombre de la ruta
    - Grado

    Devuelve un diccionario con los campos extraídos o None si la imagen es inválida.
    """

    image = cv2.imread(image_path)
    if image is None:
        return None  # La imagen no se pudo cargar

    # Aplicar OCR a la imagen
    text = pytesseract.image_to_string(image)

    # Limpiar líneas vacías y espacios
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    # Extraer campos con seguridad frente a OCR incompleto
    name  = lines[0] if len(lines) > 0 else "unknown"
    grade = lines[2] if len(lines) > 1 else "unknown"

    filename = os.path.basename(image_path)

    return {
        "filename": filename,
        "name": name,
        "grade": grade,
    }

# Función principal

def extract_metadata(header_dir):
    """
    Recorre todas las imágenes en la carpeta de encabezados (`header_dir`),
    aplica OCR en paralelo con múltiples hilos y construye un DataFrame con los resultados.

    Devuelve: pandas.DataFrame con las columnas:
    - filename, name, grade, stars, mark
    """

    # Obtener todas las imágenes .png del directorio
    image_paths = [
        os.path.join(header_dir, f)
        for f in os.listdir(header_dir)
        if f.lower().endswith(".png")
    ]

    print(f"🔎 Procesando {len(image_paths)} encabezados con OCR en paralelo...")

    results = []

    # Crear un pool de hilos para paralelizar el OCR
    with ThreadPoolExecutor() as executor:
        # Enviar todas las tareas en paralelo
        futures = [executor.submit(process_image_ocr, path) for path in image_paths]

        # Usar tqdm para mostrar una barra de progreso mientras se completan
        for future in tqdm(as_completed(futures), total=len(futures), desc="OCR"):
            result = future.result()
            if result:
                results.append(result)

    print("✅ OCR completado.")
    return pd.DataFrame(results)
