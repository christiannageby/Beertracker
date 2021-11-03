from flask import Flask, render_template, request, flash
from werkzeug.utils import redirect
from shared import db
from blueprints.recipes import recipe_actions
from blueprints.brews import brew_actions


import sqlalchemy.exc

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(recipe_actions)
app.register_blueprint(brew_actions)
db.init_app(app)

