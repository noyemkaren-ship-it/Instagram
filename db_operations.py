from simple_db import get_connection
import sqlite3

# ========== РАБОТА С ПОЛЬЗОВАТЕЛЯМИ ==========

def add_user(name, password):
    """Добавить нового пользователя"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (name, password) VALUES (?, ?)",
            (name, password)
        )
        conn.commit()
        print(f"✅ Пользователь {name} добавлен")
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        print(f"❌ Пользователь {name} уже существует")
        return None
    finally:
        conn.close()

def get_user_by_name(name):
    """Получить пользователя по имени"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {"id": user[0], "name": user[1], "password": user[2]}
    return None

def check_user(name, password):
    """Проверить логин и пароль"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE name = ? AND password = ?",
        (name, password)
    )
    user = cursor.fetchone()
    conn.close()
    return user is not None

# ========== РАБОТА С ИЗОБРАЖЕНИЯМИ ==========

def add_image(image_url, category):
    """Добавить изображение (category: 1 - девочки, 2 - мемы)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO images (image_url, category) VALUES (?, ?)",
        (image_url, category)
    )
    conn.commit()
    image_id = cursor.lastrowid
    conn.close()
    print(f"✅ Изображение {image_id} добавлено")
    return image_id

def get_images_by_category(category):
    """Получить все изображения категории"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM images WHERE category = ?", (category,))
    images = cursor.fetchall()
    conn.close()
    return [{"id": img[0], "url": img[1], "category": img[2]} for img in images]

def get_all_images():
    """Получить все изображения"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM images")
    images = cursor.fetchall()
    conn.close()
    return [{"id": img[0], "url": img[1], "category": img[2]} for img in images]

def delete_image(image_id):
    """Удалить изображение"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM images WHERE id = ?", (image_id,))
    conn.commit()
    conn.close()
    print(f"✅ Изображение {image_id} удалено")