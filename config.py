import os

password = ''
serveris = ''

ieladet_env = True

try:
    if ieladet_env:
        password = os.environ['POSTGRES_PASSWORD']
        password = os.environ['POSTGRES_CONTAINER']
        #serveris = 'api_db_image'
        del os.environ['POSTGRES_PASSWORD']
        del os.environ['POSTGRES_CONTAINER']
        ieladet_env = False
except:
    #Testa vide, kad nav norādīts env
    if ieladet_env:
        password = 'adminadmin'
        serveris = 'localhost'
        ieladet_env = False


DATABASE_URI = 'postgresql://postgres:'+password+'@'+serveris+':5432/postgres'

FAILU_FOLDERIS = 'faili'
FILE_SIZE = 104857600  # 100MB (bytes)
CHUNK_SIZE = 2 ** 20  # 1MB
