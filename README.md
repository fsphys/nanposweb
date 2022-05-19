# NANPOS Web

## Config

create `instance/config.py`. All [Flask](https://flask.palletsprojects.com/en/2.0.x/)
/ [Flask-Login](https://flask-login.readthedocs.io/en/latest/)
/ [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) config values are possible.

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

Other customizable and their default values are:

````python
TERMINAL_LOGOUT_TIMEOUT = 30  # logout timeout for Terminal mode in seconds, set to none to disable
````

## Init

create db-tables:

```python
from nanposweb import create_app
from nanposweb.db import db

app = create_app()
app.app_context().push()
db.create_all()
```

create admin user:

```python
from nanposweb.db import db
from nanposweb.db.models import User
from nanposweb.helpers import calc_hash

admin = User(name='admin', isop=True, pin=calc_hash('1234'))

db.session.add(admin)
db.session.commit()
```

### Bank Data
If you want to display bank account informations, you can define the variable `BANK_DATA` inside the instance config.
Keys and Values will be used inside the table. If `BANK_DATA` is undefined or `None` the page will not be linked in the navigation.
```python
BANK_DATA = {
    'Owner': 'Max Mustermann',
    'IBAN': '123455',
    'BIC': 'ABCDE',
    'Bank': 'Musterbank'
}
```