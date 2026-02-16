import dataset

# Подключаемся к базе
db = dataset.connect('sqlite:///mydb.db')

# Получаем таблицы
users = db['users']
images = db['images']

from database import users


# ========== ФУНКЦИИ ДЛЯ users ==========

def add_user(id, name, password):
    """Добавить пользователя"""
    # Проверяем, есть ли уже такой id
    if get_user(id):
        print(f"❌ Пользователь с id {id} уже существует")
        return False

    users.insert({
        'id': id,
        'name': name,
        'password': password  # В реальном проекте хешируй пароль!
    })
    print(f"✅ Пользователь {name} добавлен")
    return True


def get_user(id):
    """Получить пользователя по id"""
    return users.find_one(id=id)


def get_user_by_name(name):
    """Получить пользователя по имени"""
    return users.find_one(name=name)


def get_all_users():
    """Получить всех пользователей"""
    return list(users.all())


def check_user(name, password):
    """Проверить логин и пароль"""
    user = users.find_one(name=name, password=password)
    return user is not None


def update_user(id, name=None, password=None):
    """Обновить пользователя"""
    user = get_user(id)
    if not user:
        print(f"❌ Пользователь {id} не найден")
        return False

    data = {'id': id}
    if name: data['name'] = name
    if password: data['password'] = password
    users.update(data, ['id'])
    print(f"✅ Пользователь {id} обновлен")
    return True


def delete_user(id):
    """Удалить пользователя"""
    if not get_user(id):
        print(f"❌ Пользователь {id} не найден")
        return False

    users.delete(id=id)
    print(f"✅ Пользователь {id} удален")
    return True

db.commit()