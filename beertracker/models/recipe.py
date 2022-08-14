from beertracker.shared import db

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    estimated_og = db.Column(db.Integer, nullable=False)
    estimated_fg = db.Column(db.Integer, nullable=True)
    malt = db.Column(db.JSON(), nullable=False)
    hops = db.Column(db.JSON(), nullable=False)
    mash = db.Column(db.JSON(), nullable=False)
    other = db.Column(db.JSON(), nullable=True)
    before_boil = db.Column(db.Integer, nullable=False)
    yeast = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)