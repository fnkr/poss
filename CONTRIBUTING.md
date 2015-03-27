This file contains some info about how to develop and contribute to POSS.

**-** Run the server in development mode
```
# Windows
env\scripts\python manage.py runserver --debug

# Linux
env/bin/python manage.py runserver --debug
```

**-** Before committing please have a look at the
[existing commit messages](https://github.com/fnkr/POSS/commits/master)
— Make sure that they'll look the same.

**-** Compress `js`/`css` using YUI
https://github.com/yui/yuicompressor/releases
— I like PyCharm and use the File Watchers feature so that [minified versions
are created automatically as soon as I save a `js` or `css` file in the IDE]
(https://github.com/fnkr/POSS/blob/master/docs/resources/PyCharm/watchers.xml).
Other IDE's or text editors have similar features or plugins
(e.g. there is a YUI compressor plugin for [Sublime Text](https://packagecontrol.io/packages/YUI%20Compressor)).

**-** Create a migration after you changed the database
```
# Windows
env\scripts\python manage.py db migrate -m "comment"

# Linux
env/bin/python manage.py db migrate -m "comment"
```

---

The following is mostly for maintainers:

**-** Upgrade installed packages
```
# Windows
for /f "delims===" %i in ('env\scripts\pip freeze -l') do env\scripts\pip install -U %i

# Linux
env/bin/pip freeze -l | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 env/bin/pip install -U
```
