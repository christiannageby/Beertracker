"""This file defines the Brew class, to map in the database"""
from shared import db

class Brew(db.Model):
    """This class creates the database table as well as the object for describing a brew"""
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    brew_og = db.Column(db.Integer, nullable=False)
    brew_fg = db.Column(db.Integer, nullable=True)
    brew_day = db.Column(db.Date, nullable=False)
    brew_done_ferm = db.Column(db.Date, nullable=False)
    brew_comment = db.Column(db.Text)
