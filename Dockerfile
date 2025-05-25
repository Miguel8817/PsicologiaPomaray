# Usa imagen oficial de Python
FROM python:3.9-slim

# Instalar dependencias del sistema (si necesita compilación)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de archivos
COPY . .

# Puerto expuesto (Railway inyecta $PORT)
EXPOSE $PORT

# Comando para ejecutar con Gunicorn (recomendado para producción)
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]