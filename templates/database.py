import dataset

# Подключаемся к базе
db = dataset.connect('sqlite:///mydb.db')

# Создаем таблицы если их нет
users = db['users']
images = db['images']

# Создаем индексы
users.create_index(['id'])
images.create_index(['id'])
images.create_index(['category'])