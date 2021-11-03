from datetime import datetime
from flask import Flask, render_template, request, flash
from werkzeug.utils import redirect
from shared import db
from models.recipe import Recipe
from models.brew import Brew
from blueprints.recipes import recipe_actions


import sqlalchemy.exc

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(recipe_actions)
db.init_app(app)

@app.route('/brew/create', methods=['POST'])
def add_brew() -> redirect:
    try:
        recipe_id = int(request.form['recipe_id'])
        brew_day = datetime.strptime(request.form['brew_day'], '%Y-%m-%d')
        brew_og = request.form['brew_og']
        brew_fg = request.form['brew_fg']
        brew_comment = request.form['brew_comment']

        brew_done_ferm = datetime.strptime(request.form['brew_done_ferm'], '%Y-%m-%d')

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


@app.route('/brew/edit/<int:id>')
def edit_brew(id) -> render_template:
    brew = Brew.query.get_or_404(id)
    recipe = Recipe.query.get_or_404(brew.recipe_id)
    return render_template('edit/brew.html', brew=brew, recipe=recipe)


@app.route('/brew/edit', methods=['POST'])
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
            raise sqlalchemy.orm.exc.NoResultFound()

        brew.brew_og = brew_og
        brew.brew_fg = brew_fg
        brew.brew_comment = brew_comment
        brew.brew_done_ferm = brew_done_ferm
        brew.brew_day = brew_day

        db.session.add(brew)
        db.session.commit()
    except sqlalchemy.orm.exc.NoResultFound:
        flash("Error modifying brew, invalid brew id")
    except ValueError:
        flash("Error modifying brew, invalid input")
    finally:
        return redirect('/brews')


@app.route('/')
@app.route('/brews')
def brews() -> render_template:
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    today = datetime.now().date()
    brews = db.session.query(Brew, Recipe).join(Recipe).filter(Brew.recipe_id == Recipe.id).\
        order_by(Brew.brew_day.desc()).paginate(page=page, per_page=per_page)
    return render_template('brews.html', brews=brews, today=today)
