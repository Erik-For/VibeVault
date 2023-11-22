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
    return render_template()

@app.route("/login")
def login_page():
    return render_template("login.html.j2")