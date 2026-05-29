import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Usamos 'postgres_db' porque es el nombre del servicio en tu docker-compose
# Y usamos el puerto 5432 (el interno del contenedor)
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@postgres_db:5432/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia para usar en tus controllers
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()