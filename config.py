import os

password = ''
serveris = ''

try:
    password = os.environ['POSTGRES_PASSWORD']
    serveris = 'api_db_image'
except:
    password = 'adminadmin'
    serveris = 'localhost'

DATABASE_URI = 'postgresql://postgres:'+password+'@'+serveris+':5432/postgres'
print(DATABASE_URI)
#DATABASE_URI = 'postgresql://postgres:adminadmin@localhost:5432/postgres'
FAILU_FOLDERIS = 'faili'
FILE_SIZE = 104857600  # 100MB (bytes)
CHUNK_SIZE = 2 ** 20  # 1MB
