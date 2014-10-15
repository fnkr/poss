# System
import sys

# Flask
from flask import Flask, render_template

# SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate

# Define the WSGI application object
app = Flask(__name__)
app.config['APP_NAME'] = 'POSS'
app.config['APP_VERSION'] = '0.1'

# Configurations
config = 'config'
for argument in sys.argv:
    if argument[0:len('--config=')] == '--config=':
        config = str(argument[len('--config='):])

app.config.from_object(config)

if not app.config['DEBUG']:
    app.jinja_env.auto_reload = False
    # app.jinja_env.add_extension('libs.jinja2htmlcompress.HTMLCompress')


# Define the database object and Base model which
# is imported by modules and controllers
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Base(db.Model):
    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,
                              default=db.func.current_timestamp(),
                              nullable=False)
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp(),
                              nullable=False)

    def __init__(self):
        pass


# Error handling
@app.errorhandler(403)
def e_403(e):
    return render_template(
        'server_message.html',
        window_title='%s %s' % (e.code, e.name),
        title='%s' % e.name,
        description='%s' % e.description
    ), e.code


@app.errorhandler(404)
def e_404(e):
    return render_template(
        'server_message.html',
        window_title='%s %s' % (e.code, e.name),
        title='%s' % e.name,
        description='%s' % e.description
    ), e.code


@app.errorhandler(500)
def e_500(e):
    return render_template(
        'server_message.html',
        window_title='500 Internal Server Error',
        title='Internal Server Error',
        description='The server encountered an internal error and was unable to complete your request.'
    ), e.code


@app.after_request
def db_commit(response):
    db.session.commit()
    return response


# Jinja2 Functions
from app.objects.utils import human_readable_size
app.jinja_env.globals.update(human_readable_size=human_readable_size)

# Register functions
from .auth.controllers import app as auth
app.register_blueprint(auth)

from .objects.controllers import app as objects
app.register_blueprint(objects)

from .stats.controllers import app as stats
app.register_blueprint(stats)

db.create_all()

# Create initial user if there is no user in db
from app.auth.models import User
if User.query.count() == 0:
    import uuid
    user = User('admin', 'admin@example.com', str(uuid.uuid4())[0:8])
    user.role_admin = True
    db.session.add(user)
    db.session.commit()
    print('''===
Welcome to your new %s installation!
A new admin account has been created.
Login: %s
Password: %s
===''' % (app.config['APP_NAME'], user.email, user.plain_password))
