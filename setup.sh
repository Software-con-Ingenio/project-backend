#!/bin/bash

# Bloque 1: Levantar el repositorio
echo "Actualizando el repositorio local..."
git pull origin main

# Bloque 2: Levantar la base de datos mínima
echo "Iniciando contenedores de base de datos..."
docker-compose up -d

# Bloque 3: Instalar dependencias
echo "Creando entorno virtual e instalando dependencias..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Bloque 4: Ejecutar pruebas básicas (testing a futuro)
echo "Ejecutando pruebas unitarias..."
pytest

# Bloque 5: Ejecución inicial
echo "Iniciando el servidor FastAPI..."
uvicorn main:app --reload