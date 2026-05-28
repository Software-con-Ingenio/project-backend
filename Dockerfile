# Usamos una imagen base de Python oficial
FROM python:3.11-slim

# Definimos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalamos dependencias del sistema necesarias para psycopg2 (PostgreSQL)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiamos el archivo de requerimientos primero para aprovechar el caché de Docker
COPY requirements.txt .

# Instalamos las librerías de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código fuente al contenedor
COPY . .

# Exponemos el puerto donde corre FastAPI
EXPOSE 8000

# Comando para iniciar la aplicación (Asegúrate de tener un archivo 'main.py')
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]