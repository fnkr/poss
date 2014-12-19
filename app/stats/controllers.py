# Utils
import datetime
from utils.pytimeparse.timeparse import timeparse

# Flask
from flask import abort
from flask import Blueprint
from flask import render_template
from flask import request
from flask import session

# SQLAlchemy
from app import db

# POSS APIs
from app.auth.apis import session_to_user
from app.auth.utils import auth_error_return_helper

# POSS Models
from .models import View
from app.objects.models import Object

# POSS Utils
from .utils import make_daterange
from .utils import find_monday

# Define the blueprint
app = Blueprint('stats', __name__)


@app.route('/<oid>/stats')
def overview(oid):
    o = Object.query.filter_by(oid=oid).first()
    if not o: return abort(404)

    s = session_to_user(request, session, user_id=o.owner, or_admin=True)
    if s.auth_error: return auth_error_return_helper(s)

    # daterange & datescope
    daterange = timeparse(request.args.get('range', ''))
    datescope = request.args.get('scope', None)

    if type(daterange) == int:
        datestart = datetime.datetime.now() - datetime.timedelta(seconds=daterange)
    else:
        datestart = o.date_created

    #if datescope not in ('y', 'm', 'w', 'd'):
    if datescope not in ('y', 'm', 'd'):
        if datestart > (datetime.datetime.now() - datetime.timedelta(days=90)):
            datescope = 'd'
        # elif datestart > (datetime.datetime.now() - datetime.timedelta(days=630)):
        #     datescope = 'w'
        elif datestart > (datetime.datetime.now() - datetime.timedelta(days=2739)):
            datescope = 'm'
        else:
            datescope = 'y'

    datestart = datestart.replace(hour=0, minute=0, second=0, microsecond=0)
    if datescope == 'w':
        datestart = find_monday(datestart)
    elif datescope == 'm':
        datestart = datestart.replace(day=1)
    elif datescope == 'y':
        datestart = datestart.replace(month=1, day=1)

    # prepare dataset
    data = { 'labels': [] }
    for viewtype in View.type.type.enums:
        data[viewtype] = {}

    # fetch data from db
    q = db.session
    qc = [View.type, db.func.count('*').label('count'), db.extract('year', View.date_created).label('_year')]
    qg = ['type']
    # http://www.w3schools.com/sql/func_extract.asp
    if datescope in ('m', 'd'):
        qc.append(db.func.LPAD(db.extract('month', View.date_created), 2, '0').label('_month'))
        qg.append('_month')
    if datescope == 'w':
        qc.append(db.func.LPAD(db.extract('week', View.date_created), 2, '0').label('_week'))
        qg.append('_week')
    if datescope == 'd':
        qc.append(db.func.LPAD(db.extract('day', View.date_created), 2, '0').label('_day'))
        qg.append('_day')
    q = q.query(*qc)
    q = q.group_by(*qg)
    q = q.filter_by(object=o.id)
    q = q.filter(View.date_created >= datestart)
    q = q.all()

    # prepare labels
    for value in q:
        # value: TYPE, COUNT, YEAR, [MONTH,] [WEEK|DAY]
        # for some reason value[2]-value[4] is binary on some systems, I have no idea why
        if datescope == 'y':
            label = value[2].decode('utf-8') if type(value[2]) == bytes else value[2]
        elif datescope in ('m', 'w'):
            label = '%s-%s' % (value[2].decode('utf-8') if type(value[2]) == bytes else value[2],
                               value[3].decode('utf-8') if type(value[3]) == bytes else value[3])
        elif datescope == 'd':
            label = '%s-%s-%s' % (value[2].decode('utf-8') if type(value[2]) == bytes else value[2],
                                  value[3].decode('utf-8') if type(value[3]) == bytes else value[3],
                                  value[4].decode('utf-8') if type(value[4]) == bytes else value[4])

        data[value[0]][str(label)] = value[1]

    # add dates without views to labels
    if datescope == 'y':
        dateformat = '%Y'
    elif datescope == 'm':
        dateformat = '%Y-%m'
    elif datescope == 'w':
        dateformat = '%Y-%W'
    elif datescope == 'd':
        dateformat = '%Y-%m-%d'

    data['labels'] = [date.strftime(dateformat) for date in make_daterange(datestart, datetime.datetime.now(), datescope)]

    # make dict to list
    for viewtype in View.type.type.enums:
        newData = []
        for date in data['labels']:
            try:
                newData.append(data[viewtype][date])
            except KeyError:
                newData.append(0)

        # empty dict if there is no view for that viewtype at all
        if all(x == 0 for x in newData):
            newData = []
        else:
            data[viewtype] = newData

    return render_template('stats/overview.html', o=o, s=s, data=data)


@app.route('/<oid>/stats/traffic_locations')
def traffic_locations(oid):
    o = Object.query.filter_by(oid=oid).first()
    if not o: return abort(404)

    s = session_to_user(request, session, user_id=o.owner, or_admin=True)
    if s.auth_error: return auth_error_return_helper(s)

    q = db.session
    q = q.query(View.country_code, db.func.count(View.country_code).label('_count'))
    q = q.filter(View.object == o.id)
    q = q.group_by(View.country_code)
    q = q.order_by('_count desc')
    q = q.all()

    return render_template('stats/traffic_locations.html', o=o, s=s, data=q)


@app.route('/<oid>/stats/traffic_sources')
def traffic_sources(oid):
    o = Object.query.filter_by(oid=oid).first()
    if not o: return abort(404)

    s = session_to_user(request, session, user_id=o.owner, or_admin=True)
    if s.auth_error: return auth_error_return_helper(s)

    return render_template('stats/traffic_sources.html', o=o, s=s)


@app.route('/<oid>/stats/traffic_settings')
def traffic_settings(oid):
    o = Object.query.filter_by(oid=oid).first()
    if not o: return abort(404)

    s = session_to_user(request, session, user_id=o.owner, or_admin=True)
    if s.auth_error: return auth_error_return_helper(s)

    return render_template('stats/traffic_settings.html', o=o, s=s)
