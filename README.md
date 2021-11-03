# Beertracker 2.0
This is a simple webapp for keeping track of your homebrewed beer.
The Beertracker 2.0 originated from a Google Spreadsheets document which wasn't sufficient for keeping track of multiple recipes.

The Beertracker uses SQLAlchemy and Flask to serve a WSGI application which can be installed almost evrywhere with Virtual Envinronment.

## Installation
To install the program start by copy the config.py.sample file to config.py. 
Modify the settings and choose the database driver, for not so tech savy persons the default URI should be enough.

To create the database and tables run python and issue this set of commands 
```python
from beertracker import Recipe, Brew, db
db.create_all()
```

once it is done you're ready to start tracking your homebrewed beer
