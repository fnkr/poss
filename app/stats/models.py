# Import the database object (db) from the main application module
from app import db, Base
from .utils import country_code
from utils.get_or_insert import get_or_insert

class View(Base):
    __tablename__ = 'view'

    # Object
    object = db.Column(db.Integer, db.ForeignKey('object.id',
                                                 ondelete='CASCADE',
                                                 onupdate='CASCADE'))

    # View Type
    type = db.Column(db.Enum('page', 'raw', 'download', 'redirect'), nullable=True)

    # Viewer
    ip = db.Column(db.String(39))
    country_code = db.Column(db.String(2))
    referrer = db.Column(db.Integer, db.ForeignKey('referrer.id',
                                                   ondelete='CASCADE',
                                                   onupdate='CASCADE'))
    user_agent = db.Column(db.Integer, db.ForeignKey('user_agent.id',
                                                     ondelete='CASCADE',
                                                     onupdate='CASCADE'))


    # Disable date_modified column for this model
    date_modified = None


    def __init__(self, object, type, ip, referrer, user_agent):
        self.object = object
        self.type = type
        self.ip = ip
        self.country_code = country_code(ip)

        if referrer:
            self.referrer = get_or_insert(Referrer, Referrer.referrer, referrer).id
        else:
            self.referrer = None

        if user_agent:
            self.user_agent = get_or_insert(UserAgent, UserAgent.user_agent, user_agent).id
        else:
            self.user_agent = None


    def __repr__(self):
        return '<View %s/%s>' % (self.object, self.type)


class Referrer(Base):
    __tablename__ = 'referrer'

    referrer = db.Column(db.String(255), nullable=True, unique=True)

    # Disable date_modified column for this model
    date_modified = None

    def __init__(self, referrer):
        self.referrer = referrer

    def __repr__(self):
        return '<referrer "%s">' % (self.referrer)


class UserAgent(Base):
    __tablename__ = 'user_agent'

    user_agent = db.Column(db.String(255), nullable=True, unique=True)

    # Disable date_modified column for this model
    date_modified = None

    def __init__(self, user_agent):
        self.user_agent = user_agent

    def __repr__(self):
        return '<user_agent "%s">' % (self.user_agent)
