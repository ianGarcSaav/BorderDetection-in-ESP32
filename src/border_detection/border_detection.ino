#define BAUD_RATE 115200

// Dimensiones de la imagen (ajusta según sea necesario)
#define IMAGE_WIDTH 80
#define IMAGE_HEIGHT 63 
#define MAX_IMAGE_SIZE (IMAGE_WIDTH * IMAGE_HEIGHT)

// Umbral para detectar bordes (ajusta según la intensidad deseada)
#define THRESHOLD 100

#define TIMEOUT_MS 2000  // Timeout de 2 segundos

byte imageBuffer[MAX_IMAGE_SIZE];
int imageLength = 0;

void performBorderDetection(byte* data, int length) {
  // Se asume que la imagen ocupa toda la matriz y está en escala de grises.
  // Se crea un buffer temporal para la imagen procesada.
  byte output[MAX_IMAGE_SIZE];
  
  // Inicializa todo a negro.
  for (int i = 0; i < length; i++) {
    output[i] = 0;
  }
  
  // Se aplica el operador Sobel, omitiendo los bordes de la imagen.
  for (int y = 1; y < IMAGE_HEIGHT - 1; y++) {
    for (int x = 1; x < IMAGE_WIDTH - 1; x++) {
      int idx = y * IMAGE_WIDTH + x;
      
      int a = data[(y - 1) * IMAGE_WIDTH + (x - 1)];
      int b = data[(y - 1) * IMAGE_WIDTH + x];
      int c = data[(y - 1) * IMAGE_WIDTH + (x + 1)];
      int d = data[y * IMAGE_WIDTH + (x - 1)];
      // int e = data[y * IMAGE_WIDTH + x]; // no usado
      int f = data[y * IMAGE_WIDTH + (x + 1)];
      int g = data[(y + 1) * IMAGE_WIDTH + (x - 1)];
      int h = data[(y + 1) * IMAGE_WIDTH + x];
      int i = data[(y + 1) * IMAGE_WIDTH + (x + 1)];
      
      int gx = (-a) + c + (-2 * d) + (2 * f) + (-g) + i;
      int gy = (-a) + (-2 * b) + (-c) + g + (2 * h) + i;
      
      // Aproximación de la magnitud del gradiente.
      int grad = abs(gx) + abs(gy);
      
      // Si el gradiente es mayor al umbral, se marca como borde (blanco).
      output[idx] = (grad > THRESHOLD) ? 255 : 0;
    }
  }
  
  // Copia la imagen procesada de nuevo en data.
  for (int i = 0; i < length; i++) {
    data[i] = output[i];
  }
}

void setup() {
  Serial.begin(BAUD_RATE);
  // Espera a que se establezca la conexión Serial
  delay(1000);

  // Recibir la imagen enviada por el PC con un timeout ampliado.
  unsigned long lastReceiveTime = millis();
  while (true) {
    while (Serial.available() > 0) {
      if (imageLength < MAX_IMAGE_SIZE) {
        imageBuffer[imageLength++] = Serial.read();
      }
      lastReceiveTime = millis();
    }
    if (millis() - lastReceiveTime > TIMEOUT_MS) {
      break;
    }
  }
  
  // Enviar confirmación al PC indicando que la imagen fue recibida.
  Serial.println("OK");

  // Ejecutar la detección de bordes (en este ejemplo, usando el operador Sobel).
  performBorderDetection(imageBuffer, imageLength);
  
  // Enviar la imagen procesada de vuelta al PC.
  for (int i = 0; i < imageLength; i++) {
    Serial.write(imageBuffer[i]);
  }
  
  // Enviar el delimitador de fin de transmisión.
  Serial.print("\nOK\n");
}

void loop() {
  // No se requiere ejecución continua.
}