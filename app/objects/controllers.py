# Python Utils
import json
import mimetypes
mimetypes.init()
import os
from urllib.parse import urlparse
import csv

# Flask
from flask import flash
from flask import abort
from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import send_file
from flask import session
from flask import url_for

# Pygments
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter

# SQLAlchemy
from app import db

# POSS Utils
from utils.expand_list import expand_int_list
from .utils import human_readable_size
from .utils import pygments_supports
from .utils import format_object_title
from ..auth.utils import is_internal
from ..auth.utils import auth_error_return_helper

# POSS APIs
from ..stats.apis import track_view
from ..auth.apis import session_to_user

# POSS Models
from .models import Object
from ..auth.models import User

# POSS Exceptions
from .exceptions import InvalidLinkException
from .exceptions import UnknownObjectTypeException

# Define the blueprint
app = Blueprint('objects', __name__)


# Home
@app.route('/', methods=['GET'])  # noqa
def list():
    s = session_to_user(request, session)
    if s.auth_error: return auth_error_return_helper(s)

    try:
        page = int(request.args.get('page')) or 1
    except Exception:
        page = 1
    terms = request.args.get('term') or None

    orders = []
    filter = []
    filter_user = s.id
    if terms:
        for terms in csv.reader([terms], skipinitialspace=True, delimiter=' '):
            terms = terms
        for term in terms:
            subterm = term.split(':')
            subterm_len = len(subterm)

            # Filter by views
            if subterm[0] == 'views' and subterm_len == 2:
                if subterm[1][0] == '>':
                    filter.append(Object.viewcount >= subterm[1][1:])
                elif subterm[1][0] == '<':
                    filter.append(Object.viewcount <= subterm[1][1:])
                elif subterm[1][0] == '=':
                    filter.append(Object.viewcount == subterm[1][1:])

            # Order by
            elif subterm[0] == 'by' and subterm_len in (2, 3):
                if subterm_len == 3:
                    orders.append([subterm[1], subterm[2]])
                else:
                    orders.append([subterm[1], 'default'])

            # Is ...
            elif subterm[0] == 'is' and subterm_len in (2, 3):
                # Is deleted
                if subterm[1] == 'deleted':
                    if subterm_len == 3 and subterm[2] == 'no':
                        filter.append(Object.deleted == False)  # noqa
                    else:
                        filter.append(Object.deleted == True)  # noqa
                # Is type ...
                if subterm[1] in ('link', 'file'):
                    if subterm_len == 2:
                        filter.append(Object.type == subterm[1])

            # Special search features for admins
            elif s.role_admin and subterm[0] == 'user' and subterm_len == 2:
                filter_user = subterm[1]

            # No special rule, search text fields
            else:
                if not term.strip() == '':
                    term = term.replace('%', '\\%')
                    term = term.replace('*', '%')
                    filter.append(db.or_(Object.oid.like(term),
                                         Object.title.like(format_object_title(term)),
                                         Object.link.like(term)
                                         ))

    data = Object.query

    orders.append(['date_created', 'default'])
    for order in orders:
        if order[0] == 'views':
            order[0] = 'viewcount'
        elif order[0] in ('id', 'object'):
            order[0] = 'oid'
        elif order[0] == 'date':
            order[0] = 'date_created'
        elif order[0] == 'created':
            order[0] = 'date_created'
        elif order[0] == 'modified':
            order[0] = 'date_modified'
        elif order[0] == 'lastviewed':
            order[0] = 'last_viewed'

        # Order by ... string to object
        if not order[0] in ('date_created',
                            'date_modified',
                            'last_viewed',
                            'title',
                            'link',
                            'oid',
                            'viewcount',
                            'size'):
            continue
        ordero = getattr(Object, order[0])
        ordero = ordero.asc() if order[1] == 'asc' else ordero.desc()

        data = data.order_by(ordero)

    if not filter_user == '*':
        filter.append(Object.owner == filter_user)
    data = data.filter(db.and_(*filter))

    data = data.paginate(page=page, per_page=15)

    return render_template('objects/list.html', s=s,
                           data=data,
                           term=request.args.get('term'))


# Upload
@app.route('/upload', methods=['GET', 'POST'])  # noqa
@app.route('/<oid>/upload', methods=['GET', 'POST'])
def upload(oid=None):
    if oid:
        o = Object.query.filter_by(oid=oid).first()
        if not o or not o.deleted or not o.type == 'file':
            return abort(404)

        s = session_to_user(request, session, user_id=o.owner, or_admin=True, api=True)
        if s.auth_error: return auth_error_return_helper(s)
    else:
        s = session_to_user(request, session, api=True)
        if s.auth_error: return auth_error_return_helper(s)

    if request.method == 'POST':
        if not is_internal(
            request,
            allowed=[url_for('objects.upload', oid=oid)]
        ) and s.auth_method == 'COOKIE':
            return abort(403)

        files = []
        randomize_filename = request.form.get('randomize_filename',
                                              default=False)

        for file in request.files.getlist('files[]'):
            if oid:
                o.undelete()
                o.set_link(file.filename)
                if randomize_filename:
                    o.randomize_filename()
            else:
                o = Object(
                    s.id,
                    'file',
                    file.filename,
                    randomize_filename=randomize_filename
                )
                db.session.add(o)

            file_path = o.filepath()
            try:
                os.makedirs(os.path.dirname(file_path))
            except FileExistsError:
                pass
            file.save(file_path)

            file_size = os.path.getsize(o.filepath())
            o.size = file_size

            files.append({'input-name': file.filename,
                          'name': o.link,
                          'size': human_readable_size(file_size),
                          'link': url_for('objects.get',
                                          oid=o.oid,
                                          _external=True),
                          'oid': o.oid,
                          'error': False})

        return json.dumps(files)

    return render_template('objects/upload.html', s=s, oid=oid)


# Paste
@app.route('/paste', methods=['GET', 'POST'])  # noqa
@app.route('/<oid>/paste', methods=['GET', 'POST'])
def paste(oid=None):
    if oid:
        o = Object.query.filter_by(oid=oid).first()
        if not o or not o.deleted or not o.type == 'file':
            return abort(404)

        s = session_to_user(request, session, user_id=o.owner, or_admin=True)
        if s.auth_error: return auth_error_return_helper(s)
    else:
        s = session_to_user(request, session)
        if s.auth_error: return auth_error_return_helper(s)

    if request.method == 'POST':
        if not is_internal(request,
                           allowed=[url_for('objects.paste', oid=oid)]):
            return abort(403)

        paste = request.form.get('paste', default='').replace('\r\n', '\n')
        filename = request.form.get('filename', default='txt')
        randomize_filename = request.form.get('randomize_filename',
                                              default=False)

        if filename == '':
            filename = 'no_filename.txt'
            randomize_filename = True
        elif filename.find('.') < 0:
            filename = 'empty_filename.%s' % filename
            randomize_filename = True
        elif filename.find('.') == 0:
            filename = 'empty_filename%s' % filename
            randomize_filename = True

        if oid:
            o.undelete()
            o.set_link(filename)
            if randomize_filename:
                o.randomize_filename()
        else:
            o = Object(
                session.get('user_id'), 'file', filename,
                randomize_filename=randomize_filename,
            )
            db.session.add(o)

        file_path = o.filepath()
        try:
            os.makedirs(os.path.dirname(file_path))
        except FileExistsError:
            pass
        file = open(file_path, 'wb')
        file.write(paste.encode('utf-8'))
        file.close()

        file_size = os.path.getsize(o.filepath())
        o.size = file_size

        return redirect(url_for('objects.get', oid=o.oid))

    return render_template('objects/paste.html', s=s, oid=oid)


# Link
@app.route('/link', methods=['POST'])
def link():
    s = session_to_user(request, session)
    if s.auth_error: return auth_error_return_helper(s)

    if not is_internal(request):
        return abort(403)

    link = request.form.get('link', default='').replace('\r\n', '\n')

    try:
        o = Object(session.get('user_id'), 'link', link)
        db.session.add(o)
        return redirect(url_for('objects.edit', oid=o.oid))
    except InvalidLinkException:
        flash('This is no valid URL.', 'callout-danger')
        return redirect(url_for('objects.list'))


# Edit object
@app.route('/<oid>/edit', methods=['GET', 'POST'])  # noqa
def edit(oid):
    o = Object.query.filter(Object.oid == oid).first()
    if not o: return abort(404)

    s = session_to_user(request, session, user_id=o.owner, or_admin=True)
    if s.auth_error: return auth_error_return_helper(s)

    form = {
        'oid': [None, None],
        'owner': [None, None],
        'title': [None, None],
        'link': [None, None],
        'deleted': [None, None],
        'deleted_reason': [None, None],
        'type': [None, None],
        'size': [None, None],
        'date_created': [None, None],
        'date_modified': [None, None],
        'last_viewed': [None, None]
    }
    date_modified_before = o.date_modified

    if request.method == 'POST':
        if not is_internal(request, allowed=[url_for('objects.edit', oid=oid)]):
            return abort(403)

        task = request.form.get('task')

        if task == 'object.edit':
            title = request.form.get('title')
            link = request.form.get('link')

            if title == '':
                title = None
            if title != o.title:
                o.set_title(title)
                form['title'] = ['success', 'updated']

            if link == '':
                link = None

            if link != o.link:
                try:
                    if o.deleted and o.type == 'file':
                        form['link'] = ['error',
                                        'you cannot name a deleted file object']
                    else:
                        o.set_link(link)
                        form['link'] = ['success', 'updated']

                    if o.deleted and o.type == 'link':
                        o.undelete()
                        form['link'] = ['success',
                                        'updated, object recreated']

                except InvalidLinkException:
                    form['link'] = ['error', 'the link is invalid']
        elif task == 'object.convert':
            type = request.form.get('type')

            if o.deleted:
                if o.type == 'file' and type == 'link':
                    o.convert_to_link()
                    form['type'] = ['success', 'converted from file']
                elif o.type == 'link' and type == 'file':
                    o.convert_to_file()
                    form['type'] = ['success', 'converted from link']
            else:
                form['type'] = ['error',
                                'the object has to be deleted to '
                                'perform this conversation']

        db.session.commit()
        if o.date_modified != date_modified_before:
            form['date_modified'] = ['success', 'updated']

    form['oid'].insert(0, o.oid)
    form['owner'].insert(0, User.query.get(o.owner).name_email_str())
    form['title'].insert(0, o.title or '')
    form['link'].insert(0, o.link or '')
    form['deleted'].insert(0, 'Yes' if o.deleted else 'No')
    form['deleted_reason'].insert(0, (o.deleted_reason or '').upper())
    form['type'].insert(0, o.type.upper())
    form['size'].insert(0, human_readable_size(o.size))
    form['date_created'].insert(0, o.date_created)
    form['date_modified'].insert(0, o.date_modified if o.date_modified != o.date_created else '')
    form['last_viewed'].insert(0, o.last_viewed or '')

    return render_template('objects/edit.html', o=o, s=s, form=form)


@app.route('/<oid>')
def get(oid):
    o = Object.query.filter_by(oid=oid).first()
    if not o or o.deleted: return abort(404)
    if o.type == 'file' and not os.path.isfile(o.filepath()): return abort(404)

    s = session_to_user(request, session, user_id=o.owner)
    if s.auth_error:
        track_view(o, request, type=('redirect' if o.type == 'link' else 'page'))

    if o.type == 'file':
        if os.path.splitext(o.link)[1] in ('.jpg',
                                           '.jpeg',
                                           '.png',
                                           '.gif'):
            return render_template('objects/type/image.html', o=o, s=s)
        elif pygments_supports(o.link) or o.link.endswith('.log'):
            with open(o.filepath(), 'r', encoding='utf-8') as file:
                code = file.read()
            if o.link.endswith('.log'):
                lexer = get_lexer_for_filename('.txt')
            else:
                lexer = get_lexer_for_filename(o.link)
            hl_lines = expand_int_list(request.args.get('H'))
            formatter = HtmlFormatter(linespans='line', hl_lines=hl_lines)
            code = highlight(code, lexer, formatter)
            language = lexer.name

            return render_template('objects/type/code.html', o=o, s=s,
                                   language=language,
                                   code=code)
        else:
            return render_template('objects/type/file.html', o=o, s=s)

    elif o.type == 'link':
        return redirect(o.link, code=301)
    else:
        raise UnknownObjectTypeException


@app.route('/<oid>/dl')
def get_dl(oid):
    o = Object.query.filter_by(oid=oid).first()
    if not o or o.type != 'file' or o.deleted: return abort(404)

    if session_to_user(request, session, user_id=o.owner).auth_error:
        track_view(o, request, type='download')

    return send_file(o.filepath(),
                     as_attachment=True,
                     attachment_filename=o.link)


@app.route('/<oid>-')
@app.route('/<oid>/raw')
def get_raw(oid):
    o = Object.query.filter_by(oid=oid).first()
    if not o or o.type != 'file' or o.deleted: return abort(404)

    if not is_internal(request) and \
       session_to_user(request, session, user_id=o.owner).auth_error:
        track_view(o, request, type='raw')

    mimetype = mimetypes.guess_type(o.link)[0]
    if mimetype == 'text/html':
        mimetype = 'text/plain'

    return send_file(o.filepath(), mimetype=mimetype)


@app.route('/<oid>/delete')
def delete(oid):
    o = Object.query.filter_by(oid=oid).first()
    if not o or o.deleted: return abort(404)

    s = session_to_user(request, session, user_id=o.owner, or_admin=True)
    if s.auth_error: return auth_error_return_helper(s)

    if s.auth_as_admin:
        delete_reason = 'admin'
    else:
        delete_reason = 'user'

    object_url = url_for('objects.get', oid=o.oid)
    if not is_internal(request,
                       allowed=[url_for('objects.list'),
                                url_for('objects.upload'),
                                url_for('objects.upload', oid=o.oid),
                                url_for('objects.edit', oid=o.oid),
                                object_url]):
        return abort(403)

    o.delete(delete_reason)

    if urlparse(request.referrer).path in \
       (object_url, url_for('objects.upload')):
        next_url = url_for('objects.edit', oid=o.oid)
    else:
        next_url = request.referrer

    return redirect(next_url)
