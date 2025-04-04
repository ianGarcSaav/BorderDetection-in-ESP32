from PIL import Image
import os

# Parámetros
IMAGE_PATH = "../images/imagen_original.png"  # Ruta de la imagen original
OUTPUT_FOLDER = "../results"  # Carpeta donde se guardarán las particiones
NUM_PARTS = 16  # Número de divisiones en cada eje (32x32 = 1024 imágenes)
RESIZE_FACTOR = 2  # Factor de reducción (1 = no reducir, 2 = reducir a la mitad)
OUTPUT_FORMAT = "JPEG"  # Formato de salida ("JPEG", "PNG", etc.)
OUTPUT_QUALITY = 50  # Calidad de compresión (solo para JPEG)

def split_image(image_path, output_folder, num_parts, resize_factor=1, output_format="JPEG", output_quality=10):
    """Divide una imagen en partes y las guarda en una carpeta."""

    # Crear la carpeta si no existe
    os.makedirs(output_folder, exist_ok=True)

    # Cargar la imagen en escala de grises
    img = Image.open(image_path).convert("L")  

    # Reducir la resolución si es necesario
    if resize_factor > 1:
        img = img.resize((img.width // resize_factor, img.height // resize_factor))

    # Obtener tamaño de la imagen ajustada
    width, height = img.size
    part_width = width // num_parts
    part_height = height // num_parts

    # Cortar la imagen en partes
    for i in range(num_parts):
        for j in range(num_parts):
            left = j * part_width
            upper = i * part_height
            right = left + part_width
            lower = upper + part_height

            # Recortar la subimagen
            img_part = img.crop((left, upper, right, lower))

            # Construir la ruta del archivo de salida
            output_filename = f"part_{i}_{j}.{output_format.lower()}"
            output_path = os.path.join(output_folder, output_filename)

            # Guardar la imagen fragmentada con opciones de formato
            if output_format == "JPEG":
                img_part.save(output_path, output_format, quality=output_quality, optimize=True)
            else:
                img_part.save(output_path, output_format)

    print(f"Total de imágenes generadas: {num_parts * num_parts}")

# Ejecutar la función con los parámetros ajustados
split_image(IMAGE_PATH, OUTPUT_FOLDER, NUM_PARTS, RESIZE_FACTOR, OUTPUT_FORMAT, OUTPUT_QUALITY)
