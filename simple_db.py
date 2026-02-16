import sqlite3
import os
from pathlib import Path

# Используем домашнюю папку пользователя
home = str(Path.home())
db_dir = os.path.join(home, 'instagram_app')
os.makedirs(db_dir, exist_ok=True)

DB_PATH = os.path.join(db_dir, 'instagram.db')

print(f"📁 База данных будет создана в: {DB_PATH}")


def init_database():
    """Инициализация базы данных"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Создаем таблицу пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Создаем таблицу изображений
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_url TEXT NOT NULL,
            category INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ База данных инициализирована")


# Инициализируем при запуске
init_database()


def get_connection():
    """Получить соединение с БД"""
    return sqlite3.connect(DB_PATH)