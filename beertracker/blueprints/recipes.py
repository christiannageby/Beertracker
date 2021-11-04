from flask import Blueprint, request, redirect, flash, render_template
from beertracker.models.recipe import Recipe
from beertracker.shared import db

recipe_actions = Blueprint('recipe_actions', __name__)

@recipe_actions.route('/recipes')
def recipes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    recipes = Recipe.query.paginate(per_page=per_page, page=page)
    return render_template('recipes.html', recipes=recipes, per_page=per_page)


@recipe_actions.route('/recipe/create', methods=['GET'])
def create_recipe() -> render_template:
    return render_template('create/recipe.html')


@recipe_actions.route('/recipe/create', methods=['POST'])
def add_recipe() -> redirect:
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

    other = []
    no_other = int(request.form.get('no_other'))
    other_name = request.form.getlist('other_name[]')
    other_amount = request.form.getlist('other_amount[]')
    other_time = request.form.getlist('other_time[]')
    other_ok = no_other == len(other_name) and no_other == len(other_amount) and no_other == len(other_name)

    before_boil = request.form.get('before_boil')
    estimated_og = request.form.get('estimated_og')
    estimated_fg = request.form.get('estimated_fg')
    name = request.form.get('name')
    yeast = request.form.get('yeast')
    comment = request.form.get('comment')

    if hops_ok and malts_ok and mash_ok and other_ok:
        for i in range(no_hops):
            hops.append({"name": hop_names[i], "amount": hop_amount[i], "boil": hop_boil[i]})
        for i in range(no_malt):
            malt.append({"name": malt_names[i], "amount": malt_amount[i]})
        for i in range(no_mash):
            mash.append({"name": mash_stages[i], "temp": mash_temps[i], "duration": mash_durations[i]})
        for i in range(no_other):
            other.append({"name": other_name[i], "amount": other_amount[i], "time": other_time[i]})


    try:
        new_recipe = Recipe(
            name=name,
            before_boil=before_boil,
            mash=mash,
            estimated_fg=estimated_fg,
            estimated_og=estimated_og,
            hops=hops,
            malt=malt,
            yeast=yeast,
            other=other,
            comment=comment
        )
        db.session.add(new_recipe)
        db.session.commit()
    except ValueError:
        flash("Could not add recipe due to invalid inputs")
    finally:
        return redirect("/recipes")


@recipe_actions.route('/recipe/<int:id>')
def recipe(id) -> render_template:
    recipe = Recipe.query.get_or_404(id)
    return render_template('recipe.html', recipe=recipe)


@recipe_actions.route('/brew/recipe/<int:id>')
def brew_recipe(id) -> render_template:
    recipe = Recipe.query.get_or_404(id)
    return render_template('create/brew.html', recipe=recipe)
