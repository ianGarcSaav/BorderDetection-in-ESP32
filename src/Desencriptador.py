from PIL import Image
import sys

# Abrir archivo para guardar el mensaje desencriptado
with open("mensaje_desencriptado.txt", "w") as output_file:
    # Redirigir la salida estándar al archivo
    sys.stdout = output_file

    # Cargar la imagen encriptada
    image = Image.open("../images/encrypted_logo.png")
    image = image.convert("RGB")
    pixels = image.load()

    # Extraer mensaje del LSB del canal azul
    binary_message = ""
    message = ""

    for y in range(image.height):
        for x in range(image.width):
            r, g, b = pixels[x, y]
            binary_message += str(b & 1)  # Extrae el bit menos significativo del azul

            # Procesar caracteres de 8 en 8 bits
            if len(binary_message) % 8 == 0:
                byte = binary_message[-8:]  # Últimos 8 bits
                if byte == "00000000":  # Señal de fin de mensaje
                    break
                message += chr(int(byte, 2))

                # Mostrar el mensaje progresivamente
                sys.stdout.write(f"\rMensaje desencriptado: {message}")
                sys.stdout.flush()

        else:
            continue  # Solo se ejecuta si el bucle interno no se interrumpe
        break  # Rompe el bucle externo si se encontró el byte de terminación

    sys.stdout.write("\nProceso terminado.")
