import os
from PIL import Image, ImageEnhance, ImageFilter

# Carpeta de entrada con las 256 imágenes (fragmentos)
input_folder = "../processedImages"
# Ruta de salida para la imagen final postprocesada
output_path = "../final_image.jpeg"

# Recopilar archivos que sigan el patrón "part_<fila>_<columna>_processed.jpeg"
files = [f for f in os.listdir(input_folder) if f.endswith("_processed.jpeg")]

# Lista para almacenar (fila, columna, nombre de archivo)
parts = []
for f in files:
    try:
        base, _ = os.path.splitext(f)
        # Se espera un nombre en el formato: part_<fila>_<columna>_processed
        tokens = base.split("_")
        # tokens = ["part", fila, columna, "processed"]
        row = int(tokens[1])
        col = int(tokens[2])
        parts.append((row, col, f))
    except Exception as e:
        print(f"Se omite el archivo {f}: {e}")

if not parts:
    print("No se encontraron imágenes con el patrón esperado.")
    exit(1)

# Determinar la cantidad de filas y columnas a partir de los índices máximos
max_row = max(p[0] for p in parts)
max_col = max(p[1] for p in parts)
grid_rows = max_row + 1
grid_cols = max_col + 1

# Cargar una imagen de muestra para obtener el tamaño de cada parte
sample_path = os.path.join(input_folder, parts[0][2])
sample_img = Image.open(sample_path)
part_width, part_height = sample_img.size

# Crear una imagen nueva del tamaño total
total_width = grid_cols * part_width
total_height = grid_rows * part_height
final_img = Image.new("L", (total_width, total_height))

# Pegar cada fragmento en su posición correcta
for row, col, filename in parts:
    img_path = os.path.join(input_folder, filename)
    part_img = Image.open(img_path)
    final_img.paste(part_img, (col * part_width, row * part_height))

# --- Postprocesado ---
# 1. Upscaling para mejorar la resolución (se utiliza LANCZOS para alta calidad)
scale_factor = 2  # Puedes ajustar el factor de escalado
upscaled = final_img.resize((final_img.width * scale_factor, final_img.height * scale_factor), Image.LANCZOS)

# 2. Mejorar contraste
enhancer = ImageEnhance.Contrast(upscaled)
upscaled = enhancer.enhance(1.2)  # Aumenta el contraste (ajusta según sea necesario)

# 3. Aplicar filtro de nitidez
upscaled = upscaled.filter(ImageFilter.SHARPEN)

# Guardar la imagen final postprocesada
upscaled.save(output_path, "JPEG")
print("Imagen final guardada en:", output_path)