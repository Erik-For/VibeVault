from flask import request, redirect, url_for, render_template, flash, send_from_directory, Response, stream_with_context
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app import app, db
from app.models import User
import os

login_manager = LoginManager(app)

#connect the flask_login library to the database User model
@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).where(User.id == user_id)).first()[0]

# Redirect users to login page if not logged in
@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login")

#index path
@app.route("/")
@login_required # makes sure the user is logged in
def index():
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
        user = db.session.execute(db.select(User).where(User.email == email)).scalar_one_or_none()
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
#Music streaming and artist related endpoints
#

def stream_audio(file_path):
    with open(file_path, "rb") as audio_file:
        while True:
            data = audio_file.read(1024)
            if not data:
                break
            yield data

@app.route("/content/info/<id>")
@login_required
def content_info(id):
    return id

@app.route("/content/stream/<id>")
@login_required
def content_stream(id):
    file_path = get_path(id)
    return Response(stream_with_context(stream_audio(file_path)), mimetype="audio/mpeg")

def get_path(id):
    return os.getcwd() + "/app/static/temp.mp3"