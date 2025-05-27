# Используется модулем db.py для создания соединения с MySQL.
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}
