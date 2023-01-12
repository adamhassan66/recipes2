from flask_app.models.user_model import User  # CHANGE THIS
from flask_app.models.recipe_model import Recipe
from flask_bcrypt import Bcrypt
from flask import flash
from flask import render_template, redirect, request, session
from flask_app import app
bcrypt = Bcrypt(app)

@app.route('/')
def main():
    if "user_id" in session:
        return redirect('/dashboard')
    return render_template("login.html")

@app.route('/dashboard')
def dashboard_show():
    if "user_id" not in session:
        return('/')
    data = {
        'id': session['user_id']
    }
    logged_user = User.get_by_id(data)
    all_recipes = Recipe.get_all()
    return render_template('dashboard.html', all_recipes = all_recipes,logged_user = logged_user)


@app.route('/user/create', methods=['POST'])
def create_user():
    if not User.validate(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        **request.form,
        "password": pw_hash
    }
    # Call the save @classmethod on User
    user_id = User.save_user(data)
    user_in_db = User.get_by_email(data)
    # session['first_name'] = user_in_db.first_name
    # store user id into session
    session['user_id'] = user_id
    return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password",'login')
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password" 'login')
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    session['first_name']=user_in_db.first_name
    return redirect('/dashboard')

@app.route('/users/logout')
def logout():
    del session['user_id']
    return redirect('/')