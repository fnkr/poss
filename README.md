# POSS - Personal Object Sharing System

[![Build Status](https://travis-ci.org/fnkr/POSS.svg?branch=master)](https://travis-ci.org/fnkr/POSS)
[![Requirements Status](https://requires.io/github/fnkr/POSS/requirements.svg?branch=master)](https://requires.io/github/fnkr/POSS/requirements/?branch=master)
[![Coverage Status](https://coveralls.io/repos/fnkr/POSS/badge.svg)](https://coveralls.io/r/fnkr/POSS)

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
# Make sure that virtualenv uses a supported Python version,
# maybe you have to set the path to Python manually. For example:
# `virtualenv --python=$(which python3.4) env` or `virtualenv3.4 env`
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
env\scripts\python manage.py db stamp head

# Linux
env/bin/python manage.py db stamp head
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
[CONTRIBUTING.md](https://github.com/fnkr/POSS/blob/master/CONTRIBUTING.md)
