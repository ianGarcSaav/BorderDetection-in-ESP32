import serial
import time
import argparse
import numpy as np
from PIL import Image
import os
import glob

# Parámetros por defecto
DEFAULT_SEND_IMAGE_PATH = "../processedImages/part_1_1.jpeg"  # Solo para referencia
SERIAL_PORT = "COM3"                                   # Puerto serial al que está conectado el ESP32
BAUD_RATE = 115200                                     # Velocidad de baudios
WAIT_BOOT_LOGS = 2                                     # Tiempo para esperar boot logs del ESP32

# Función que procesa una imagen enviándola al ESP32 y recibiendo la imagen procesada
def process_image(image_path, output_path):
    print(f"\nProcesando imagen: {image_path}")
    # Abrir la imagen y preprocesarla
    img = Image.open(image_path)
    img = img.convert("L")  # Convertir a escala de grises
    img = img.resize((80, 63))  # Redimensionar a 80x63
    img_bytes = img.tobytes()

    # Verificar que el tamaño sea correcto
    if len(img_bytes) != 80 * 63:
        print(f"Error: La imagen procesada tiene {len(img_bytes)} bytes, pero se esperaban {80 * 63}.")
        return False

    # Abrir conexión serial
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=None)
    time.sleep(2)  # Esperar a que el ESP32 esté listo
    ser.reset_input_buffer()

    # Enviar la imagen al ESP32
    print("Enviando imagen al ESP32...")
    ser.write(img_bytes)
    ser.flush()

    # Esperar confirmación del ESP32
    while True:
        if ser.in_waiting > 0:
            response = ser.readline().decode("utf-8").strip()
            print(f"Respuesta del ESP32: {response}")
            if response == "OK":
                break

    # Recibir la imagen procesada
    print("Esperando imagen procesada...")
    processed_data = bytearray()
    while True:
        if ser.in_waiting > 0:
            chunk = ser.read(ser.in_waiting)
            processed_data.extend(chunk)
            if b"\nOK\n" in processed_data:
                processed_data = processed_data[:80 * 63]
                break

    # Reconstruir la imagen procesada
    processed_img = Image.frombytes("L", (80, 63), bytes(processed_data))
    processed_img.save(output_path)
    print(f"Imagen procesada guardada en: {output_path}")

    ser.close()
    return True

if __name__ == "__main__":
    # Carpeta de entrada donde se encuentran las imágenes a procesar
    input_folder = os.path.join("..", "imageDivisions")
    # Carpeta de salida donde se guardarán las imágenes procesadas
    output_folder = os.path.join("..", "processedImages")
    os.makedirs(output_folder, exist_ok=True)

    # Buscar todas las imágenes en la carpeta ../imageDivisions con extensión .jpeg
    image_paths = glob.glob(os.path.join(input_folder, "*.jpeg"))
    if not image_paths:
        print("No se encontraron imágenes en la carpeta ../imageDivisions")
        exit(1)

    # Procesar cada imagen secuencialmente
    for path in sorted(image_paths):
        # Se omiten las imágenes que ya contengan "_processed" en su nombre
        base_name = os.path.basename(path)
        if "_processed" in base_name:
            continue
        name, ext = os.path.splitext(base_name)
        output_filename = f"{name}_processed{ext}"
        output_path = os.path.join(output_folder, output_filename)
        success = process_image(path, output_path)
        if not success:
            print(f"Error al procesar la imagen {path}.")
        else:
            print(f"Procesamiento de {path} completado.")
