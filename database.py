import dataset
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'mydb.db')

db = dataset.connect(f'sqlite:///{DB_PATH}')

users = db['users']
images = db['images']

users.create_index(['id'])
images.create_index(['id'])
images.create_index(['category'])

print(f"✅ База данных подключена: {DB_PATH}")