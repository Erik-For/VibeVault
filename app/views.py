from flask import request, redirect, url_for, render_template, flash, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app import app, db
from app.models import User

login_manager = LoginManager()
login_manager.init_app(app)

#connect the flask_login library to the database User model
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Redirect users to login page if not logged in
@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login")

#index path
@app.route("/")
@login_required # makes sure the user is logged in
def index():
    print(current_user)
    return render_template("home.html.j2")

#
#Login related endpoints
#

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':        
        return render_template("login.html.j2")
    elif request.method == 'POST':
        password = request.form['password']
        email = request.form['email'].lower()
        user = db.session.execute(db.select(User).where(User.email == email)).first()[0]
        if user is None:
            flash("Invalid email or password")
            return redirect(url_for("login_page"))
        if user.check_password(password) == False:
            flash("Invalid email or password")
            return redirect(url_for("login_page"))
        else:
            login_user(user)
            flash("Login successful")
            return redirect(url_for('index'))
    

@app.route("/login/forgot-password", methods=['GET', 'POST'])
def forgot_password():
    if request.method == "GET":
        return render_template("forgot_password.html.j2")

#
#
#