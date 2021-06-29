from datetime import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    malt = db.Column(db.JSON(), nullable=False)
    hops = db.Column(db.JSON(), nullable=False)
    mash = db.Column(db.JSON(), nullable=False)
    before_boil = db.Column(db.Integer, nullable=False)
    yeast = db.Column(db.String(255), nullable=False)
    other = db.Column(db.Text)



class Brew(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    brew_og = db.Column(db.Integer, nullable=False)
    brew_fg = db.Column(db.Integer, nullable=True)
    brew_day = db.Column(db.Date, nullable=False)
    brew_done_ferm = db.Column(db.Date, nullable=False)
    brew_comment = db.Column(db.Text)


@app.route('/recipes')
def list_recipes():
    recipes = Recipe.query.all()
    return render_template('recipes.html', recipes=recipes)

@app.route('/recipe/delete/<int:id>')
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    try:
        db.session.delete(recipe)
        db.session.commit()
    except:
        pass
    finally:
        return redirect('/recipes')

@app.route('/recipe/create',  methods=['GET'])
def create_recipe():
    return render_template('create/recipe.html')

@app.route('/recipe/create', methods=['POST'])
def add_recipe():
    hops = []
    no_hops = int(request.form.get('no_hops'))
    hop_names = request.form.getlist('hop[]')
    hop_amount = request.form.getlist('hop_amount[]')
    hop_boil = request.form.getlist('hop_boil[]')
    hops_ok = no_hops == len(hop_names) and no_hops == len(hop_amount) and no_hops == len(hop_boil)

    malt = []
    no_malt = int(request.form.get('no_malts'))
    malt_names = request.form.getlist('malt[]')
    malt_amount = request.form.getlist('malt_amount[]')
    malts_ok = no_malt == len(malt_names) and no_malt == len(malt_amount)


    mash = []
    no_mash = int(request.form.get('no_mash'))
    mash_stages = request.form.getlist('mash[]')
    mash_temps = request.form.getlist('mash_temp[]')
    mash_durations = request.form.getlist('mash_duration[]')
    mash_ok = no_mash == len(mash_stages) and no_mash == len(mash_temps) and no_mash == len(mash_durations)

    if hops_ok and malts_ok and mash_ok:
        for i in range(no_hops):
            hops.append({"name": hop_names[i], "amount": hop_amount[i], "boil": hop_boil[i]})
        for i in range(no_malt):
            malt.append({"name": malt_names[i], "amount": malt_amount[i]})
        for i in range(no_mash):
            mash.append({"name": mash_stages[i], "temp": mash_temps[i], "duration": mash_durations[i]})

    before_boil = request.form.get('before_boil')
    name = request.form.get('name')
    yeast = request.form.get('yeast')
    other = request.form.get('other')

    try:
        print(request.form)
        new_recipe = Recipe(
            name=name,
            before_boil=before_boil,
            mash=mash,
            hops=hops,
            malt=malt,
            yeast=yeast,
            other=other
        )
        db.session.add(new_recipe)
        db.session.commit()
    except Exception as e:
        return "{}".format(e)

    return redirect("/recipes")



@app.route('/recipe/<int:id>')
def recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template('recipe.html', recipe=recipe)

@app.route('/brew/recipe/<int:id>')
def brew_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template('brew.html', recipe=recipe)

@app.route('/brew/create', methods=['POST'])
def add_brew():
    if request.method == 'POST':
        recipe_id = request.form['recipe_id']
        brew_day = datetime.strptime(request.form['brew_day'], '%Y-%m-%d')
        brew_og = request.form['brew_og']
        brew_fg = request.form['brew_fg']
        brew_comment = request.form['brew_comment']

        brew_done_ferm = datetime.strptime(request.form['brew_done_ferm'], '%Y-%m-%d')

        brew = Brew(recipe_id=recipe_id, brew_og=brew_og, brew_fg=brew_fg, brew_day=brew_day, brew_done_ferm=brew_done_ferm, brew_comment=brew_comment)
        try:
            db.session.add(brew)
            db.session.commit()
            return redirect('/brews')
        except Exception as e:
            return "Problem adding the brew to database: {}".format(e)

@app.route('/brew/edit/<int:id>')
def edit_brew(id):
    brew = Brew.query.get_or_404(id)
    recipe = Recipe.query.get_or_404(brew.recipe_id)
    return render_template('edit/brew.html', brew=brew, recipe=recipe)

@app.route('/brew/edit', methods=['POST'])
def modify_brew():
    if request.method == 'POST':
        brew_id = request.form['brew_id']
        brew_og = request.form['brew_og']
        brew_fg = request.form['brew_fg']
        brew_done_ferm = datetime.strptime(request.form['brew_done_ferm'], '%Y-%m-%d')
        brew_day = datetime.strptime(request.form['brew_day'], '%Y-%m-%d')

        brew = Brew.query.get_or_404(brew_id)
        brew.brew_og = brew_og
        brew.brew_fg = brew_fg
        brew.brew_done_ferm = brew_done_ferm
        brew.brew_day = brew_day

        try:
            db.session.add(brew)
            db.session.commit()
        except Exception as e:
            print(e)
        finally:
            return redirect('/brews')

@app.route('/')
@app.route('/brews')
def brews():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    brews = db.session.query(Brew, Recipe).join(Recipe).filter(Brew.recipe_id==Recipe.id).order_by(Brew.brew_day.desc()).paginate(page=page, per_page=per_page)
    return render_template('brews.html', brews=brews)
