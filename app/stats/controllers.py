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

# Define the blueprint
app = Blueprint('stats', __name__)


@app.route('/<oid>/stats')
def overview(oid):
    o = Object.query.filter_by(oid=oid).first()
    if not o: return abort(404)

    s = session_to_user(request, session, user_id=o.owner, or_admin=True)
    if s.auth_error: return auth_error_return_helper(s)

    daterange = timeparse(request.args.get('range', ''))
    datescope = request.args.get('scope', None)

    if type(daterange) == int:
        timedelta = datetime.timedelta(seconds=daterange)
    else:
        timedelta = None

    if datescope not in ('y', 'm', 'w', 'd'):
        datescope = 'd'

    data = {
        'page': {},
        'raw': {},
        'download': {},
        'redirect': {},
        'labels': []
    }

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
    if timedelta:
        q = q.filter(View.date_created > datetime.datetime.now() - timedelta)
    q = q.all()

    for value in q:
        # value: TYPE, COUNT, YEAR, [MONTH,] [WEEK|DAY]
        if datescope == 'y':
            label = value[2]
        elif datescope in ('m', 'w'):
            label = '%s-%s' % (value[2], value[3])
        elif datescope == 'd':
            label = '%s-%s-%s' % (value[2], value[3], value[4])

        data[value[0]][label] = value[1]
        data['labels'].append(label)

    data['labels'] = list(set(data['labels']))
    data['labels'].sort()

    # return ''
    return render_template('stats/overview.html', o=o, s=s,
                           data=data,
                           datescope=datescope,
                           daterange=request.args.get('range', None)
                           )


@app.route('/<oid>/stats/traffic_locations')
def traffic_locations(oid):
    o = Object.query.filter_by(oid=oid).first()
    if not o: return abort(404)

    s = session_to_user(request, session, user_id=o.owner, or_admin=True)
    if s.auth_error: return auth_error_return_helper(s)

    return render_template('stats/traffic_locations.html', o=o, s=s)


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
