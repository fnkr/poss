# Import the database object (db) from the main application module
from app import db, Base
from .utils import country_code

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
    referrer = db.Column(db.String(255))
    user_agent = db.Column(db.String(255))

    # New instance instantiation procedure
    def __init__(self, object, type, ip, referrer, user_agent):

        self.object = object
        self.type = type
        self.ip = ip
        self.country_code = country_code(ip)
        self.referrer = referrer
        self.user_agent = user_agent

    def __repr__(self):
        return '<View %s/%s>' % (self.object, self.type)
