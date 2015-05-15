**1)** Create a new container using the Python template.
**2)** After creation open the container settings and add the container public key to GitHub.
**3)** Add a port to the container and set the preview checkbox to checked. Do not forget to click "apply changes".
**4)** Open the IDE, then create a new file with the following contents:
```bash
cd ~/code
git clone git@github.com:fnkr/POSS.git .
sudo apt-get -y install mysql-server
mysql -u root -proot -e "create user poss@localhost identified by 'poss';"
mysql -u root -proot -e "create database poss;"
mysql -u root -proot -e "grant all privileges on poss.* to poss@localhost;"
cp config.dist.py config.py
sed -i "s/DEBUG = False/DEBUG = True/" config.py
sed -i "s/HOST = '127.0.0.1'/HOST = '0.0.0.0'/" config.py
sed -i "s/PORT = 8080/PORT = os.environ['NITROUS_PREVIEW_PORT']/" config.py
sed -i "s/SERVER_NAME = 'localhost:8080'/SERVER_NAME = '%s.nitrousapp.com:%s' % (os.environ['HOSTNAME'], os.environ['NITROUS_PREVIEW_PORT'])/" config.py
sed -i "s/PREFERRED_URL_SCHEME = 'http'/PREFERRED_URL_SCHEME = 'https'/" config.py
virtualenv --python=$(which python3) ../env
../env/bin/pip install -r requirements.txt
echo "--------------------------------------------------------------------------------"
../env/bin/python manage.py db stamp head 2>&1 | grep ": "
```
**5)** Make the file executable (`chmod +x FILENAME`), then execute it.
You will be prompted for a MySQL root password. Use `root` as password for root.
**6)** Run POSS.
```bash
env/bin/python code/manage.py runserver
```