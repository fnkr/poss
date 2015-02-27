# POSS - Personal Object Sharing System

[![Build Status](https://magnum.travis-ci.com/fnkr/POSS.svg?token=Upy55UysDyQpDJCzdKA3&branch=master)](https://magnum.travis-ci.com/fnkr/POSS)

## Demo
https://demo.ge1.me  
Email: demo  
Password: demo  
Reset: every hour

## Requirements
* git (for installing/upgrading)
* Python 3.3 or 3.4
* pip
* virtualenv
* MySQL Server

## Install
**1)** Clone the project and checkout the latest tag
```
git clone https://github.com/fnkr/POSS.git

# Windows
for /f %c in ('git rev-list --tags --max-count=1') do git checkout %c

# Linux
git checkout $(git rev-list --tags --max-count=1)

cd poss
```

**2)** Set up your environment
```
virtualenv env

# Windows
env\scripts\pip install -r requirements

# Linux
env/bin/pip install -r requirements
```

**3)** Download GeoIP databse (optional)  
Download and extract "GeoLite Country" and "GeoLite Country IPv6" databases
and put the files `GeoIP.dat` and `GeoIPv6.dat` into the main directory.
http://dev.maxmind.com/geoip/legacy/geolite/

**4)** Copy config.dist.py to config.py and modify as needed. Note that POSS has only been tested with MySQL (5.5), everything else may not work.

**5)** Set up the database
```
# Windows
env\scripts\python manage.py db upgrade

# Linux
env/bin/python manage.py db upgrade
```

**6)** Run the server  
You can run/test the server with:

```
# Windows
env\scripts\python manage.py runserver

# Linux
env/bin/python manage.py runserver
```

The `runserver` method is **NOT recommended for productional use**.
Use a application server container like FastCGI or uWSGI instead:
https://github.com/fnkr/POSS/tree/master/docs/deployment

## Upgrade

**1)** Fetch and checkout the latest tag
```
git fetch --tags

# Windows
for /f %c in ('git rev-list --tags --max-count=1') do git checkout %c

# Linux
git checkout $(git rev-list --tags --max-count=1)
```

**2)** Update environment
```
# Windows
env\scripts\pip install -r requirements

# Linux
env/bin/pip install -r requirements
```

**3)** Migrate the database
```
# Windows
env\scripts\python manage.py db upgrade

# Linux
env/bin/python manage.py db upgrade
```

## Command line client

There is a command line client for POSS, you can get it from here:
https://github.com/fnkr/POSS-Client

## Development notes
**-** Run the server in development mode
```
# Windows
env\scripts\python manage.py runserver --debug

# Linux
env/bin/python manage.py runserver --debug
```

**-** Create a migration after you changed the database
```
# Windows
env\scripts\python manage.py db migrate -m "comment"

# Linux
env/bin/python manage.py db migrate -m "comment"
```

**-** Compress js/css using YUI
https://github.com/yui/yuicompressor/releases

**-** Upgrade installed packages
```
# Windows
for /f "delims===" %i in ('env\scripts\pip freeze -l') do env\scripts\pip install -U %i

# Linux
env/bin/pip freeze -l | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 env/bin/pip install -U
```
