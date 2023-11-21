from flask import request, redirect, url_for, render_template, flash, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app import app, db
from app.models import User

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login")


@app.route("/")
@login_required
def index():
    print(current_user)
    return "Hello"

@app.route("/login")
def login_page():
    return render_template("login.html")