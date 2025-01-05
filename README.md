# nanposweb - Fachschaft Physik Edition

This is a fork of the [Fachschaft Physik am KIT](https://fachschaft.physik.kit.edu) of the "NANPOS Web" project, created 
by [domrim](https://gitlab.com/domrim) and licensed under the MIT-License. The original project can be found here: 
https://gitlab.com/domrim/nanposweb

## Requirements

- Python 3.9 or higher

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
3. (Optional, but recommended) Create a folder `instance` and inside it the file `config.py` to configure your instance.
   Further information on the configuration options can be found in the configuration section.
4. Decide, if you want to run it locally or in a docker container
   1. Local installation:
      1. (Optional, but recommended) Create a virtual environment
      2. Install all requirements listed in the `pyproject.toml`. There is currently no command for this, as `pip` is 
         not able to install the requirements without the project itself, which might causes headaches during 
         development.
      3. Create a file `run.py` inside the project folder with the following content:
         ```python
         from nanposweb import create_app

         # Create an app instance
         app = create_app()

         # Start it automatically
         app.run(threaded=True, debug=True)
         ```
      4. Run `python run.py` or `python3 run.py` to start the application
   2. Docker:
      1. Build the image from the `Dockerfile`
      2. Mount your config file into the container to point to `/app/instance/config.py`
      3. Run your container
5. If you are running this the first time, you need to prepare your database.
   1. Open an interactive `python` shell
   2. Run the following code to generate all required database tables:
      ```python
      from nanposweb import create_app
      from nanposweb.db import db

      app = create_app()
      app.app_context().push()
      db.create_all()
      ```
   3. Create an admin user with a password. You must do this, if you have not enabled user sign up, or you won't be able
      to create an account to log in with. User sign up is disabled by default, if you haven't changed it in you 
      'config.py'. Run the following code to create an admin user with the name "admin" and the password "1234":
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
6. Now you are ready to go! 

## Config

These are the default values used for the config:

```python
SECRET_KEY='dev'
SESSION_COOKIE_SECURE=True
REMEMBER_COOKIE_SECURE=True
SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_DATABASE_URI='postgresql://nanpos:nanpos@localhost:5432/nanpos'
# logout timeout for Terminal mode in seconds, set to none to disable
TERMINAL_LOGOUT_TIMEOUT=30
# Second-Limit for canceling a revenue
QUICK_CANCEL_SEC=60
# Cooldown between multiple purchases in seconds. If zero, there's no cooldown.
PURCHASE_COOLDOWN=0.0
# Option, whether purchases with no cost must be verified
VERIFY_FREE_PURCHASES=False
# Optional text, that is displayed during confirmation
VERIFY_FREE_PURCHASES_NOTE=None
# Display bank data
BANK_DATA=None
# Amount of favorite products which should get highlighted
FAVORITES_DISPLAY=3
# Timespan for calculation of favorite products in Days
FAVORITES_DAYS=100
# Disable user sign up
ALLOW_SIGNUP=False
# Disable the card reader by default
ENABLE_CARD_READER=False
# Verify the send card reader device id
VERIFY_CARD_READER=False
# List of strings of verified readers. Per default are no card readers authorized.
VERIFIED_CARD_READERS=[]
# Display prices and a balance instead of a count
SHOW_BALANCE_AND_PRICE=True
# Allow purchases over budget
ALLOW_NEGATIVE_BALANCES=False
```

You can use additional standard configuration values from the [Flask](https://flask.palletsprojects.com/en/2.0.x/), [Flask-Login](https://flask-login.readthedocs.io/en/latest/)
and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) that aren't listed here to suit your needs. 

### Database setup

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
