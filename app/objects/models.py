# Python Utils
import uuid
import os

# Flask
from flask import current_app

# SQLAlchemy
from app import db, Base

# POSS Utils
from .utils import is_valid_url
from .utils import format_object_title

# POSS Exceptions
from .exceptions import InvalidLinkException
from .exceptions import ObjectIsNotDeletedException
from .exceptions import UnknownObjectTypeException

# Settings
oid_MIN_LENGTH = 5
oid_MAX_LENGTH = 32
oid_DEFAULT_LENGTH = 20
oid_ALLOWED_CHARS = 'a-zA-Z0-9-_'


# def oid_validate(key):
#     key = re.sub('[^%s]' % oid_ALLOWED_CHARS, '', key)
#     key = key[0:oid_DEFAULT_LENGTH]
#
#     if len(key) <= oid_MIN_LENGTH:
#         return False
#     else:
#         return True


def oid_generate():
    while True:
        oid = str(uuid.uuid4()).replace('-', '')[0:oid_DEFAULT_LENGTH]

        if not Object.query.filter(Object.oid == oid).first():
            return oid


def fid_generate():
    while True:
        p1_length = 10

        rnd = str(uuid.uuid4()).replace('-', '')
        p1 = rnd[:p1_length]
        p2 = rnd[p1_length:]
        p1 = '1/%s' % '/'.join([p1[i:i+2] for i in range(0, len(p1), 2)])
        fid = '%s/%s' % (p1, p2)

        if not Object.query.filter(Object.fid == fid).first():
            return fid


class Object(Base):
    __tablename__ = 'object'

    # Users
    owner = db.Column(db.Integer, db.ForeignKey('user.id',
                                                ondelete='CASCADE',
                                                onupdate='CASCADE'))

    # Object type and oid
    type = db.Column(db.Enum('file', 'link', name='poss_object_type'), nullable=False)
    size = db.Column(db.Integer, nullable=True)
    encrypted = db.Column(db.Boolean, default=False)

    # Location
    oid = db.Column(db.String(64), nullable=False, unique=True)
    fid = db.Column(db.String(39), nullable=True, unique=True)
    title = db.Column(db.String(64), nullable=True)
    link = db.Column(db.Text, nullable=True)

    # Lifecycle
    deleted = db.Column(db.Boolean, nullable=False, default=False)
    deleted_reason = db.Column(db.Enum('user', 'admin', 'autodelete', 'system', name='poss_object_deleted_reason'), nullable=True)
    autodelete_type = db.Column(db.Enum('on_view', 'by_viewer', 'at_time', name='poss_object_autodelete_type'), nullable=True)
    autodelete_param = db.Column(db.Integer, nullable=True)

    # Views
    viewcount = db.Column(db.Integer, nullable=False, default=0)
    views = db.relationship('View')
    last_viewed = db.Column(db.DateTime, nullable=True)

    def __init__(self, owner, type, link, randomize_filename=False):
        self.oid = oid_generate()
        self.type = type
        self.owner = owner
        self.set_link(link)

        if self.type == 'file':
            self.fid = fid_generate()

            if randomize_filename:
                self.randomize_filename()
        elif self.type == 'link':
            pass
        else:
            raise UnknownObjectTypeException

    def set_title(self, title):
        if title:
            self.title = format_object_title(title)
        else:
            self.title = None

    def set_link(self, link):
        if self.type == 'link':
            if not is_valid_url(link):
                raise InvalidLinkException
            else:
                self.link = link
        elif self.type == 'file':
            if len(link) > 0:
                self.link = link
            else:
                raise InvalidLinkException
        else:
            self.link = link

    def randomize_filename(self):
        self.link = '%s%s' % (self.oid, os.path.splitext(self.link)[1])

    def filepath(self):
        return os.path.join(current_app.config['DATA_DIR'], self.fid)

    def delete(self, reason):
        if self.type == 'file':
            if os.path.isfile(self.filepath()):
                os.remove(self.filepath())

        self.deleted = True
        self.deleted_reason = reason
        self.size = None
        self.link = None

    def undelete(self):
        self.deleted = False
        self.deleted_reason = None

    def convert_to_link(self):
        if not self.deleted:
            raise ObjectIsNotDeletedException
        elif not self.type == 'file':
            raise UnknownObjectTypeException
        else:
            self.fid = None
            self.type = 'link'

    def convert_to_file(self):
        if not self.deleted:
            raise ObjectIsNotDeletedException
        elif not self.type == 'link':
            raise UnknownObjectTypeException
        else:
            self.fid = fid_generate()
            self.type = 'file'

    def __repr__(self):
        return '<Object %r>' % (self.oid)
