# Usa una imagen oficial de Python ligera
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala paquetes necesarios para que pip funcione correctamente
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia el archivo de requerimientos e instala las dependencias
COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*
    


RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código del proyecto al contenedor
COPY . .

# Expone el puerto (modifica si usas otro)
EXPOSE 14068

# Establece la variable de entorno para producción si la usas
ENV FLASK_ENV=production

# Comando por defecto para correr la app (ajusta si usas otro archivo o framework)
CMD ["python", "app.py"]
