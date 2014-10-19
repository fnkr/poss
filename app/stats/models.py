# Import the database object (db) from the main application module
from app import db, Base
from .utils import country_code as country_code_from_ip
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
    country_code = db.Column(db.Integer, db.ForeignKey('country_code.id',
                                                       ondelete='CASCADE',
                                                       onupdate='CASCADE'))
    referrer = db.Column(db.Integer, db.ForeignKey('referrer.id',
                                                   ondelete='CASCADE',
                                                   onupdate='CASCADE'))
    user_agent = db.Column(db.Integer, db.ForeignKey('user_agent.id',
                                                     ondelete='CASCADE',
                                                     onupdate='CASCADE'))

    def __init__(self, object, type, ip, referrer, user_agent):
        self.object = object
        self.type = type
        self.ip = ip

        country_code = country_code_from_ip(ip)
        if country_code:
            self.country_code = get_or_insert(CountryCode, CountryCode.country_code, country_code).id
        else:
            self.country_code = None

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


class CountryCode(Base):
    __tablename__ = 'country_code'

    country_code = db.Column(db.String(2), nullable=True, unique=True)

    def __init__(self, country_code):
        self.country_code = country_code

    def __repr__(self):
        return '<country_code %s>' % (self.country_code)


class Referrer(Base):
    __tablename__ = 'referrer'

    referrer = db.Column(db.String(255), nullable=True, unique=True)

    def __init__(self, referrer):
        self.referrer = referrer

    def __repr__(self):
        return '<referrer "%s">' % (self.referrer)


class UserAgent(Base):
    __tablename__ = 'user_agent'

    user_agent = db.Column(db.String(255), nullable=True, unique=True)

    def __init__(self, user_agent):
        self.user_agent = user_agent

    def __repr__(self):
        return '<user_agent "%s">' % (self.user_agent)
