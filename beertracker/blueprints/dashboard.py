"""Actions for brews"""
from datetime import datetime
from flask import Blueprint, render_template
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from beertracker.models.brew import Brew
from beertracker.models.recipe import Recipe
from beertracker.shared import db

dashboard_actions = Blueprint('dashboard_actions', __name__)

@dashboard_actions.route('/')
def dashboard() -> render_template:
    brews_per_month = db.session.query(func.strftime('%Y-%m', Brew.brew_day), func.count(Brew.id)).group_by(func.strftime('%m', Brew.brew_day)).limit(12).all()
    today = datetime.now().date()
    fermenting_brews = db.session.query(Brew, Recipe).join(Recipe).filter(Brew.recipe_id == Recipe.id and today >= Brew.brew_done_ferm).order_by(Brew.brew_day.desc())
    return render_template('dashboard.html', fermenting_brews=fermenting_brews, today=today, monthly_chart=brews_per_month)