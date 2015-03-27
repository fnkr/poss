# Python Utils
from datetime import datetime, timedelta

# SQLAlchemy
from app import db

# POSS Utils
from .utils import ip
from .utils import referrer

# POSS Models
from .models import View


def track_view(object, request, type):
    if db.session.query(View).filter(
        View.object == object.id,
        View.ip == ip(request),
        View.type == type,
        View.date_created > (datetime.now() - timedelta(hours=24))
    ).count() == 0:
        object.viewcount += 1
        view = View(object=object.id,
                    type=type,
                    ip=ip(request),
                    referrer=referrer(request),
                    user_agent=request.headers.get('User-Agent'))
        db.session.add(view)
        object.last_viewed = db.func.current_timestamp()
