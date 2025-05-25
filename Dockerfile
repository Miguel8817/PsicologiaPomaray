FROM python:3.11-slim

WORKDIR /app

# Instala dependencias del sistema necesarias y limpia cache para evitar errores
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 14068

ENV FLASK_ENV=production

# Comando para Gunicorn con 4 workers
CMD ["gunicorn", "--bind", "0.0.0.0:14068", "--workers", "4", "app:app"]