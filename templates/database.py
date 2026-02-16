import dataset

db = dataset.connect('sqlite:///mydb.db')

users = db['users']
images = db['images']

users.create_index(['id'])
images.create_index(['id'])
images.create_index(['category'])