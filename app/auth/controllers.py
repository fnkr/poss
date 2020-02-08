# Flask / Werkzeug
from flask import abort
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash

# SQLAlchemy
from app import db

# POSS Forms
from .forms import LoginForm

# POSS Models
from .models import User
from .models import ApiKey
from ..objects.models import Object

# POSS APIs
from .apis import session_to_user

# POSS Utils
from .utils import auth_error_return_helper
from .utils import is_internal
from .utils import valid_email

# Define the blueprint
app = Blueprint('auth', __name__)


# Set the route and accepted methods
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If sign in form is submitted
    form = LoginForm(request.form)

    s = session_to_user(request, session)

    # Redirect to target directly if already logged in
    if request.method == 'GET':
        if not s.auth_error and not request.args.get('force', False):
            if request.args.get('next', None):
                return redirect(request.args.get('next', None))
            else:
                return redirect(url_for('objects.list'))

    # Verify the sign in form
    if form.email.data:
        user = User.query.filter_by(email=form.email.data).first()
    else:
        user = None

    if user:
        if not check_password_hash(user.password, form.password.data):
            if form.password.data:
                flash('Invalid email or password.', 'message/error')
            else:
                flash('Invalid email or password.', 'message/error')

            form.autofocus = 'password'
        elif not user.enabled:
            flash('Your account has been locked.', 'message/error')
        else:
            session['user_id'] = user.id
            session['expired'] = False

            if form.rememberme:
                session.permanent = True

            flash('Welcome %s.' % user.name, 'callout-info')
            if request.args.get('next', None):
                return redirect(request.args.get('next', None))
            else:
                return redirect(url_for('objects.list'))
    else:
        if request.method == 'POST':
            flash('Invalid email or password.', 'message/error')

    return render_template('auth/login.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    s = session_to_user(request, session)
    if s.auth_error: return auth_error_return_helper(s)

    if not is_internal(request):
        return abort(403)

    session['expired'] = True

    if request.args.get('next', None):
        return redirect(request.args.get('next', None))
    else:
        return redirect(url_for('auth.login'))


@app.route('/account', methods=['GET', 'POST'])
@app.route('/account/<custom_user_id>', methods=['GET', 'POST'])
def account(custom_user_id=None):
    if custom_user_id:
        s = session_to_user(request, session, user_id=custom_user_id, or_admin=True)
        if s.auth_error: return auth_error_return_helper(s)
    else:
        s = session_to_user(request, session)
        if s.auth_error: return auth_error_return_helper(s)

    if custom_user_id:
        user = User.query.get(custom_user_id)
        if not user:
            return abort(404)
    else:
        user = User.query.get(session.get('user_id'))

    form = {
        'name': [user.name, None, None],
        'password': [user.password, None, None],
        'email': [user.email, None, None]
    }

    if request.method == 'POST':
        if not is_internal(request, allowed=[url_for('auth.account'), url_for('auth.account', custom_user_id=custom_user_id)]): return abort(403)

        name = request.form.get('name', None)
        email = request.form.get('email', None)
        password = request.form.get('password', None)

        if name and name != user.name:
            if len(name) > User.name.type.length or len(name) < 2:
                form['name'] = [name, 'error', 'has to be between 2 and %s characters' % User.name.type.length]
            else:
                user.name = name
                form['name'] = [name, 'success', 'update successful']

        if email and email != user.email:
            if len(email) > User.email.type.length or len(email) < 2:
                form['email'] = [email, 'error', 'has to be between 2 and %s characters' % User.email.type.length]
            elif not valid_email(email):
                form['email'] = [email, 'error', 'is syntactically incorrect']
            else:
                user.email = email
                form['email'] = [email, 'success', 'update successful']

        if password:
            if len(password) > 100 or len(password) < 8:
                form['password'] = [password, 'error', 'has to be between 8 and 100 characters']
            else:
                user.set_password(password)
                form['password'] = [password, 'success', 'update successful']

        task = request.form.get('task', '')
        if task == 'user.apikeys.new':
            apikey = ApiKey(user.id, request.form.get('keyname', '')[:25])
            db.session.add(apikey)
            db.session.commit()
        elif task == 'user.apikeys.delete':
            apikey = ApiKey.query.get(request.form.get('apikey.id', None))
            if apikey and (apikey.user == user.id or custom_user_id):
                db.session.delete(apikey)
                db.session.commit()

    apikeys = ApiKey.query.filter(ApiKey.user == user.id).all()
    return render_template('auth/account.html', s=s,
                           form=form,
                           custom_user_id=custom_user_id,
                           apikeys=apikeys)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    s = session_to_user(request, session, require_admin=True)
    if s.auth_error: return auth_error_return_helper(s)

    form_usercreate = {
        'name': ['', None, None],
        'password': ['', None, None],
        'email': ['', None, None]
    }

    if request.method == 'POST':
        if not is_internal(request, allowed=[url_for('auth.admin')]): return abort(403)

        task = request.form.get('task', '')
        if task == 'user.create':
            name = request.form.get('name', '')
            email = request.form.get('email', '')
            password = request.form.get('password', '')
            error = False

            if len(name) > User.name.type.length or len(name) < 2:
                form_usercreate['name'] = [name, 'error', 'name has to be between 2 and %s characters' % User.name.type.length]
                error = True

            if len(email) > User.email.type.length or len(email) < 2:
                form_usercreate['email'] = [email, 'error', 'email has to be between 2 and %s characters' % User.email.type.length]
                error = True
            elif not valid_email(email):
                form_usercreate['email'] = [email, 'error', 'email is syntactically incorrect']
                error = True
            elif User.query.filter(User.email == email).first():
                form_usercreate['email'] = [name, 'error', 'there is already a user with this email']
                error = True

            if len(password) > 100 or len(password) < 8:
                form_usercreate['password'] = [password, 'error', 'password has to be between 8 and 100 characters']
                error = True

            if error:
                form_usercreate['name'][0] = name
                form_usercreate['email'][0] = email
                form_usercreate['password'][0] = password
            else:
                user = User(name, email, password)
                db.session.add(user)
        elif task == 'user.lock':
            user = User.query.get(request.form.get('user.id', None))
            if user:
                user.enabled = False
        elif task == 'user.unlock':
            user = User.query.get(request.form.get('user.id', None))
            if user:
                user.enabled = True

        db.session.commit()

    try:
        users_page = int(request.args.get('users.page')) or 1
    except Exception:
        users_page = 1

    # This works fine but the result is a SQLAlchemy Query instead of a
    # Flask-SQLAlchemy BaseQuery so there is no pagination method.
    # users = []
    # for user in db.session.query(User, db.session.query(db.func.count(Object.id)).filter(Object.owner == User.id).as_scalar()).all():
    #     user[0].objects_count = user[1]
    #     users.append(user[0])

    users = User.query.order_by(User.date_modified.desc()).paginate(page=users_page, per_page=15)

    for user in users.items:
        user.objects_count = db.session.query(db.func.count(Object.id)).filter_by(owner=user.id).first()[0]

    return render_template('auth/admin.html', s=s,
                           form_usercreate=form_usercreate,
                           users=users)
