import os

HOST = '0.0.0.0'
PORT = 8080

SERVER_NAME = os.environ['SERVER_NAME']
CSRF_SESSION_KEY = os.environ['CSRF_SESSION_KEY']
SECRET_KEY = os.environ['SECRET_KEY']

DATA_DIR = '/var/poss'
SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(os.environ['DB_ADAPTER'], os.environ['DB_USER'], os.environ['DB_PASS'], os.environ['DB_HOST'], os.environ['DB_PORT'], os.environ['DB_NAME'])

# Wait until database is up
import socket
from time import sleep
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        sock.connect((os.environ['DB_HOST'], int(os.environ['DB_PORT'])))
        print('Database is up!')
        break
    except socket.error as e:
        print("Database is not up yet: {}".format(e))
        sleep(1)
sock.close()
