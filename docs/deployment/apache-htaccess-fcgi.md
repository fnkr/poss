**1)** Install POSS. https://github.com/fnkr/POSS#install

**2)** Install `flipflop`.
```
./env/bin/pip install flipflop
```

**3)** Place this script in your POSS root directory (where the `manage.py` is). Name it `poss.fcgi`.
```
#!env/bin/python
from flipflop import WSGIServer
from app import app

class ScriptNameStripper(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ['SCRIPT_NAME'] = ''
        return self.app(environ, start_response)

app = ScriptNameStripper(app)

if __name__ == '__main__':
    WSGIServer(app).run()
```

**4)** Make the script executable.
```
chmod +x poss.fcgi
```

**5)** Place this script in your POSS root directory (where the `manage.py` is). Name it `.htaccess`.
```
RewriteEngine On
RewriteBase /

Options +ExecCGI
AddHandler fcgid-script .fcgi

RewriteRule ^((?!poss\.fcgi/).*)$ /poss.fcgi/$1 [L]
```
