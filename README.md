# NANPOS Web

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