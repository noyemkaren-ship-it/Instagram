import dataset

# Подключаемся к базе
db = dataset.connect('sqlite:///mydb.db')

# Получаем таблицы
users = db['users']
images = db['images']

def add_image(id, image_url, category):
    """Добавить изображение (category: 1 - девочки, 2 - мемы)"""
    # Проверяем категорию
    if category not in [1, 2]:
        print(f"❌ Категория должна быть 1 (девочки) или 2 (мемы)")
        return False

    images.insert({
        'id': id,
        'image': image_url,
        'category': category
    })
    print(f"✅ Изображение {id} добавлено в категорию {category}")
    return True

def get_image(id):
    """Получить изображение по id"""
    return images.find_one(id=id)

def get_images_by_category(category):
    """Получить все изображения категории (1 или 2)"""
    return list(images.find(category=category))

def get_all_images():
    """Получить все изображения"""
    return list(images.all())

def update_image(id, image_url=None, category=None):
    """Обновить изображение"""
    if not get_image(id):
        print(f"❌ Изображение {id} не найдено")
        return False

    data = {'id': id}
    if image_url: data['image'] = image_url
    if category:
        if category not in [1, 2]:
            print(f"❌ Категория должна быть 1 или 2")
            return False
        data['category'] = category

    images.update(data, ['id'])
    print(f"✅ Изображение {id} обновлено")
    return True

def delete_image(id):
    """Удалить изображение"""
    if not get_image(id):
        print(f"❌ Изображение {id} не найдено")
        return False

    images.delete(id=id)
    print(f"✅ Изображение {id} удалено")
    return True

def delete_images_by_category(category):
    """Удалить все изображения категории"""
    count = len(get_images_by_category(category))
    images.delete(category=category)
    print(f"✅ {count} изображений категории {category} удалено")
    return count

def get_next_id():
    """Получить следующий свободный ID"""
    all_images = get_all_images()
    if not all_images:
        return 1
    return max(img['id'] for img in all_images) + 1

db.commit()