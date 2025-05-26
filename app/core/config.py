import os
from dotenv import load_dotenv
from sqlalchemy.engine.url import make_url

load_dotenv()  # Carga las variables de entorno del archivo .env

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

db_url = make_url(DATABASE_URL)

class Config:
    DEBUG: bool = False  # Cambiar a True durante el desarrollo si es necesario
    DB_URL: str = DATABASE_URL
    DB_HOST: str = db_url.host
    DB_PORT: int = db_url.port
    DB_USER: str = db_url.username
    DB_PASS: str = db_url.password
    DB_NAME: str = db_url.database

config = Config()