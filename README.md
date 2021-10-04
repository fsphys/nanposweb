# NANPOS Web

## Config
create `instance/config.py`. All [Flask](https://flask.palletsprojects.com/en/2.0.x/) / [Flask-Login](https://flask-login.readthedocs.io/en/latest/) / [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) config values are possible.

For production at least DB-Connection & Secret-Key are required / recommended:
```python
SECRET_KEY = 'secret-key'
SQLALCHEMY_DATABASE_URI = 'postgresql://nanpos:nanpos@localhost:5432/nanpos'
```

A Secret key can be generated with:
```python
import secrets
secrets.token_urlsafe(16)
```

## Init

create db-tables:

```python
from nanposweb.db import db

db.create_all()
```

create admin user:

```python
from nanposweb.db import db
from nanposweb.models import User

admin = User(name='admin', isop=True, pin='1234')

db.session.add(admin)
db.session.commit()
```