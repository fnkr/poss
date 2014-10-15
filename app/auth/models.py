# Python Utils
import uuid

# Werkzeug
from werkzeug.security import generate_password_hash

# SQLALchemy
from app import db, Base


class User(Base):
    __tablename__ = 'user'

    # User Data
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(192), nullable=False)

    # Account status and Roles
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    role_admin = db.Column(db.Boolean, nullable=False, default=False)

    # Objects
    objects = db.relationship('Object')

    # New instance instantiation procedure
    def __init__(self, name, email, password):

        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.plain_password = password

    def set_password(self, password):
        self.password = generate_password_hash(password)
        self.plain_password = password

    def name_email_str(self):
        return '%s <%s>' % (self.name, self.email)

    def __repr__(self):
        return '<User %s <%s>>' % (self.name, self.email)


class ApiKey(Base):
    __tablename__ = 'apikey'

    # User Data
    user = db.Column(db.Integer, db.ForeignKey('user.id',
                                               ondelete='CASCADE',
                                               onupdate='CASCADE'))
    key = db.Column(db.String(128), nullable=False, unique=True)
    name = db.Column(db.String(25), nullable=True)
    last_used = db.Column(db.DateTime,
                          nullable=True)

    # New instance instantiation procedure
    def __init__(self, user, name):

        self.user = user
        self.name = name

        while True:
            self.key = str(uuid.uuid4()).replace('-', '')[0:20]

            if not ApiKey.query.filter(ApiKey.key == self.key).first():
                break

    def use(self):
        self.last_used = db.func.current_timestamp()

    def __repr__(self):
        return '<ApiKey user=%s name="%s">' % (self.user, self.name)
