"""Main application document for importing all models and blueprints"""
from flask import Flask
from shared import db
from blueprints.recipes import recipe_actions
from blueprints.brews import brew_actions
from blueprints.dashboard import dashboard_actions

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(recipe_actions)
app.register_blueprint(brew_actions)
app.register_blueprint(dashboard_actions)
db.init_app(app)

with app.app_context():
    # Initialize the database
    db.create_all()

if __name__ == '__main__':
    app.run()
