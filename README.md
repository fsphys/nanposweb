# nanposweb - Fachschaft Physik Edition

This is a fork of the [Fachschaft Physik am KIT](https://fachschaft.physik.kit.edu) of the "NANPOS Web" project, created 
by [domrim](https://gitlab.com/domrim) and licensed under the MIT-License. The original project can be found here: 
https://gitlab.com/domrim/nanposweb

## Setup

This a quick start guide.

1. Clone the project and access the folder.
2. Get all dependencies (Bootstrap, FontAwesome Icons). This step can be skipped, if you're planning to deploy using 
   docker, as it's included in the Dockerfile.
   - Bootstrap v5: Get the following files from the latest release and put them into their matching folder.
     - `bootstrap.min.css` to `nanposweb/static/css/bootstrap.min.css`
     - `bootstrap.bundle.min.js` to `nanposweb/static/js/bootstrap.bundle.min.js`
   - FontAwesome Icon v6:
     - `all.min.css` to `nanposweb/static/css/all.min.css`
     - `all.min.js` to `nanposweb/static/js/all.min.js`
     - All contents of the `webfonts`-folder into `nanposweb/static/webfonts`
3. You are ready to go!

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
from nanposweb import create_app

app = create_app()
app.app_context().push()

admin = User(name='admin', isop=True, pin=calc_hash('1234'))

db.session.add(admin)
db.session.commit()
```

### Bank Data
If you want to display bank account information, you can define the variable `BANK_DATA` inside the instance config.
Keys and Values will be used inside the table. If `BANK_DATA` is undefined or `None` the page will not be linked in the navigation.
```python
BANK_DATA = {
    'Owner': 'Max Mustermann',
    'IBAN': '123455',
    'BIC': 'ABCDE',
    'Bank': 'Musterbank'
}
```

## License

The original code was created by [domrim](https://gitlab.com/domrim) and licensed under the MIT-License. Additionally,
all changes of the Fachschaft Physik are also licensed under this license. More information can be found in the
[LICENSE](LICENSE)-file.
