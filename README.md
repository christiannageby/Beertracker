# Beertracker
The Beertracker is an application for keeping track of home-brewed beer, you can manage different brews and recipes. You can also keep track of which bottle is which brew(Just mark them with the brew-id).
As for some history the Beertracker it originated from a Google Sheets document which was really cumbersome to manage.

## Installation
To install the program start by copy the config.py.sample file to config.py. 
Modify the settings and choose the database driver, for not so tech savy persons the default URI should be enough.

To create the database and tables run python console in the root of this repository and issue the following commands.
 
```python
from beertracker import db
db.create_all()
```

To run this application i production you should run a dedicated wsgi-gateway but for testing purposes you can use `python run.py` to run the app within a development server on port 5000.
