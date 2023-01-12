from flask_app.models.recipe_model import Recipe  # CHANGE THIS
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt
from flask import render_template, redirect, request, session, flash
from flask_app import app

bcrypt = Bcrypt(app)




# routes us to the form to createt a new recipe===========

@app.route('/recipes/new')
def new_recipe():
      return render_template('recipe_new.html')

#  Aslong as in session(logged in) its gonna create a new recipe from the form=======

@app.route('/recipes/create', methods = ['POST'])
def create_recipe():
      if "user_id" not in session:
            return('/')
      if not Recipe.validator(request.form):
            return redirect('/recipes/new')
      recipe_data = {
            **request.form,
            'user_id' : session['user_id']
            }
      Recipe.save_recipe(recipe_data)
      return redirect('/dashboard')


# ==========================
# This will take us to the show recipe page

@app.route('/recipes/<int:id>')
def show_recipe(id):
      if "user_id" not in session:
            return('/')
      data = {'id': session['user_id']
      }
      this_recipe = Recipe.get_by_id({'id': id})
      logged_user = User.get_by_id(data)
      return render_template('recipe_show.html', this_recipe = this_recipe, logged_user = logged_user)

@app.route('/recipes/<int:id>/edit')
def edit_recipe(id):
      if "user_id" not in session:
            return('/')
      data = {'id': id}
      one_recipe = Recipe.get_by_id(data)
      return render_template('recipe_edit.html', one_recipe = one_recipe)

@app.route('/recipes/<int:id>/update', methods = ['POST'])
def update_recipe(id):
      if "user_id" not in session:
            return('/')
      if not Recipe.validator(request.form):
            return redirect(f'/recipes/{id}/edit')
      data = {
            **request.form,
            'id' : id,
            }
      Recipe.update_recipe(data)
      return redirect('/dashboard')

# this will delete a recipe====

@app.route('/recipes/<int:id>/delete')
def delete_recipe(id):
      if "user_id" not in session:
            return('/')
      data = {'id': id}
      this_recipe = Recipe.get_by_id(data)
      Recipe.delete_recipe(data)
      return redirect('/dashboard')


