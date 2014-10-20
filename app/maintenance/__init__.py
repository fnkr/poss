# Utils
import os.path
import inspect

# POSS
from app import app
from app import db

# POSS Models
from app.objects.models import Object
from app.stats.models import View
from app.stats.models import Referrer
from app.stats.models import UserAgent


def maintenance():
    maintenance_referrer_useragent()
    maintenance_file_deleted_from_datadir()

def log(msg):
    print('[%s] %s' % (inspect.stack()[1][3], msg))


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


def maintenance_file_deleted_from_datadir():
    '''
    Set files to deleted in database if they are deleted locally.
    '''
    for object in Object.query.filter(Object.deleted == False).all():
        if not os.path.isfile(object.filepath()):
            log('mark object %s as deleted, "%s" does not exist' % (object.oid, object.filepath()))
            object.delete('system')

    db.session.commit()
