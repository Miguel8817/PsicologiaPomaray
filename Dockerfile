FROM python:3.11-slim

WORKDIR /app



# 1. Instala dependencias del sistema PRIMERO (¡crítico para mysqlclient!)
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*


# 2. Copia SOLO requirements.txt inicialmente
COPY requirements.txt .

# 3. Instalación robusta de dependencias
RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# 4. Copia el resto de la aplicación
COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "--workers", "4", "app:app"]