# Контекстный менеджер для работы с базой данных.
# Обеспечивает единое соединение и транзакцию на сессию.
# Используется в main.py для всех операций с БД.

import mysql.connector
from contextlib import contextmanager
from config import DB_CONFIG

@contextmanager
def db_session():
    """
    Контекстный менеджер для работы с MySQL.
    - Открывает соединение и курсор.
    - Передаёт курсор в вызывающий код.
    - Автоматически коммитит транзакцию после успешной работы.
    - В случае ошибки откатывает изменения (rollback).
    - Гарантирует закрытие курсора и соединения.
    """
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
