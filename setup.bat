@echo off

REM Bloque 1: Actualizar repositorio
echo Actualizando el repositorio local...
git pull origin main

REM Bloque 2: Levantar contenedores Docker
echo Iniciando contenedores de base de datos...
docker compose up -d

REM Bloque 3: Crear entorno virtual
echo Creando entorno virtual e instalando dependencias...

IF NOT EXIST venv (
    python -m venv venv
)

call venv\Scripts\activate

pip install -r requirements.txt

REM Bloque 4: Ejecutar pruebas
echo Ejecutando pruebas unitarias...
pytest

REM Si pytest falla, detener ejecución
IF %ERRORLEVEL% NEQ 0 (
    echo Las pruebas fallaron. Abortando...
    exit /b %ERRORLEVEL%
)

REM Bloque 5: Iniciar FastAPI
echo Iniciando el servidor FastAPI...
uvicorn main:app --reload
