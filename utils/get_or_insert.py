from app import db

def get_or_insert(table, column, value, **kwargs):
    if type(value) == str and getattr(column.type, 'length'):
        value = value[:column.type.length]

    entry = table.query.filter(column == value).first()
    if entry:
        return entry
    else:
        if not kwargs:
            kwargs = { column.key: value }
        entry = table(**kwargs)
        db.session.add(entry)
        db.session.commit()
        return entry
