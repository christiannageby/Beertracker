"""Actions for brews"""
from datetime import datetime
from flask import Blueprint, request, redirect, flash, render_template
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from models.brew import Brew
from models.recipe import Recipe
from shared import db

brew_actions = Blueprint('brew_actions_views', __name__)

@brew_actions.route('/brew/create', methods=['POST'])
def add_brew() -> redirect:
    """Allows the user to edit the parameters in a specified brew."""
    try:
        recipe_id: int = int(request.form['recipe_id'])
        brew_day: datetime = datetime.strptime(request.form['brew_day'], '%Y-%m-%d')
        brew_og: int = request.form['brew_og']
        brew_fg: int = request.form['brew_fg']
        brew_comment: str = request.form['brew_comment']
        brew_done_ferm: datetime = datetime.strptime(request.form['brew_done_ferm'], '%Y-%m-%d')
        brew = Brew(
            recipe_id=recipe_id,
            brew_og=brew_og,
            brew_fg=brew_fg,
            brew_day=brew_day,
            brew_done_ferm=brew_done_ferm,
            brew_comment=brew_comment
            )
        db.session.add(brew)
        db.session.commit()
    except ValueError:
        flash("Invalid input, try again later")
    except SQLAlchemyError:
        flash("Database error")
    finally:
        return redirect('/brews')


@brew_actions.route('/brew/edit/<int:brew_id>')
def edit_brew(brew_id: int) -> render_template:
    brew: Brew = Brew.query.get_or_404(brew_id)
    recipe: Recipe = Recipe.query.get_or_404(brew.recipe_id)
    return render_template('edit/brew.html', brew=brew, recipe=recipe)


@brew_actions.route('/brew/edit', methods=['POST'])
def modify_brew() -> redirect:
    try:
        brew_id = int(request.form['brew_id'])
        brew_og = int(request.form['brew_og'])
        brew_fg = int(request.form['brew_fg'])
        brew_done_ferm = datetime.strptime(request.form['brew_done_ferm'], '%Y-%m-%d')
        brew_day = datetime.strptime(request.form['brew_day'], '%Y-%m-%d')
        brew_comment = request.form['brew_comment']

        brew = Brew.query.get(brew_id)

        if brew is None:
            raise NoResultFound()

        brew.brew_og = brew_og
        brew.brew_fg = brew_fg
        brew.brew_comment = brew_comment
        brew.brew_done_fermenting = brew_done_ferm
        brew.brew_day = brew_day

        db.session.add(brew)
        db.session.commit()
    except NoResultFound:
        flash("Error modifying brew, invalid brew id")
    except ValueError:
        flash("Error modifying brew, invalid input")
    finally:
        return redirect('/brews')


@brew_actions.route('/')
@brew_actions.route('/brews')
def brews() -> render_template:
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    today = datetime.now().date()
    all_brews = db.session.query(Brew, Recipe).join(Recipe).filter(Brew.recipe_id == Recipe.id).\
        order_by(Brew.brew_day.desc()).paginate(page=page, per_page=per_page)
    return render_template('brews.html', brews=all_brews, today=today)
