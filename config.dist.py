import sys
import os

# Debug mode
DEBUG = False

# Enable debug mode if --debug
for argument in sys.argv:
    if argument == '--debug':
        DEBUG = True

# Host, Port
HOST = '127.0.0.1'
PORT = 8080

# Domain
SERVER_NAME = 'localhost:8080'

# Database
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://poss:poss@localhost/poss'
SQLALCHEMY_ECHO = DEBUG
DATABASE_CONNECT_OPTIONS = {}

# Login, Cookie and Session settings
CSRF_ENABLED = True
# Random strings for cookie generation, 40 chars should be enough,
# https://api.fnkr.net/random/?length=40&count=2
CSRF_SESSION_KEY = 'UV5IIDFh81YaxNXrYSp01hYMYPtxqxJWDuaBgwIj'
SECRET_KEY = 'mEFvm0yN9x6DSwmSbI7vhDR7r8aPKsqm8fy8LEL7'
SESSION_COOKIE_NAME = 'poss'
PERMANENT_SESSION_LIFETIME = 2678400
SESSION_COOKIE_SECURE = False

# URL scheme that should be used for URL generation
# if no URL scheme is available
PREFERRED_URL_SCHEME = 'http'

# Data storage, will be created if it does not exist
DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Config file version
CONFIG_VERSION = 1
