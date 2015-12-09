#!/bin/sh

# Go to workspace
cd ~/workspace

# Prepare MySQL
mysql-ctl start
mysql -u "$C9_USER" -e "create user poss@localhost identified by 'poss';"
mysql -u "$C9_USER" -e "create database poss;"
mysql -u "$C9_USER" -e "grant all privileges on poss.* to poss@localhost;"

# Prepare POSS config
cp config.dist.py config.py

sed -i "s/DEBUG = False/DEBUG = True/" config.py
sed -i "s/HOST = '127.0.0.1'/HOST = '0.0.0.0'/" config.py
sed -i "s/PORT = 8080/PORT = os.environ['C9_PORT']/" config.py
sed -i "s/SERVER_NAME = 'localhost:8080'/# SERVER_NAME = os.environ['C9_HOSTNAME']/" config.py
sed -i "s/PREFERRED_URL_SCHEME = 'http'/PREFERRED_URL_SCHEME = 'https'/" config.py

# Prepare virtualenv
virtualenv --python=$(which python3) env
env/bin/pip install -r requirements.txt

# Prepare database and print POSS access credentials
echo "--------------------------------------------------------------------------------"
env/bin/python manage.py db stamp head 2>&1 | grep ": "
