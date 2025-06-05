import pytesseract
import cv2
import os
import re
import pandas as pd

def extract_metadata(image_dir):
    """
    Extrae metadatos de imágenes recortadas del MoonBoard.
    
    Args:
        image_dir (str): Ruta a la carpeta con imágenes recortadas (solo el encabezado).
    
    Returns:
        pd.DataFrame: DataFrame con columnas ['filename', 'name', 'setter', 'grade', 'stars', 'label']
    """
    metadata = []  # Lista donde se almacenará la información extraída

    # Configuración del motor OCR (Tesseract)
    config = r'--oem 3 --psm 6'  # oem 3 = modo automático, psm 6 = texto en bloque

    # Recorrer cada archivo en la carpeta
    for filename in sorted(os.listdir(image_dir)):
        if not filename.lower().endswith(".png"):
            continue  # Saltar si no es imagen PNG

        img_path = os.path.join(image_dir, filename)
        img = cv2.imread(img_path)

        if img is None:
            continue  # Saltar si la imagen no pudo cargarse

        # Preprocesamiento para OCR
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)            # Convertir a escala de grises
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)  # Binarizar (mejora contraste)

        # Ejecutar OCR sobre la imagen
        text = pytesseract.image_to_string(thresh, config=config)

        # Limpiar y dividir el texto extraído en líneas
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        text_full = " ".join(lines)  # Línea completa unificada para buscar con regex

        # Buscar patrón para cada campo usando expresiones regulares
        match_name = lines[0] if lines else "unknown"  # Nombre del problema
        match_grade = lines[2] if lines else "unknown"  # Grado

        # Buscar línea que contenga "holds"
        label = next((l for l in lines if "hold" in l.lower()), "unknown")

        # Agregar los resultados a la lista
        metadata.append({
            "filename": filename,
            "name": re.sub(r'[^\w\s\-]', '', match_name).strip(),
            "grade": re.sub(r'[^\w\s\-]', '', match_grade).strip()
        })

    # Convertir resultados a un DataFrame
    return pd.DataFrame(metadata)
