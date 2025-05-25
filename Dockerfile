# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requerimientos y luego instala las dependencias
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código al contenedor
COPY . .

# Expone el puerto 5000 (Flask usa 5000 por defecto)
EXPOSE 5000

# Ejecuta la app con la variable de entorno PORT o 5000 si no está definida
CMD ["sh", "-c", "flask run --host=0.0.0.0 --port=${PORT:-5000}"]
