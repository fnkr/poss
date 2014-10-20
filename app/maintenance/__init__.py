from app import app
from app import db
from app.stats.models import View
from app.stats.models import Referrer
from app.stats.models import UserAgent


def maintenance():
    maintenance_referrer_useragent()


def maintenance_referrer_useragent():
    '''
    Delete rows from Referrer and UserAgent that have never been used in View,
    which can happen if you delete something from View.
    '''
    for table in ([Referrer.__tablename__, UserAgent.__tablename__]):
        # TODO: make an SQLAlchemy query from this
        db.engine.execute('''
            DELETE FROM `%(table)s` WHERE (not(exists
                (SELECT 1 FROM `%(viewtable)s`
                WHERE (`%(table)s`.`id` = `%(viewtable)s`.`%(table)s`))
            ));
        ''' % {'table': table, 'viewtable': View.__tablename__})
