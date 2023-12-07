from flask import request, redirect, url_for, render_template, flash, send_from_directory, Response, stream_with_context, send_file, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app import app, db, mail
from app.models import User, Artist, Content, FeaturedContent, FeaturedArtists, Invite
from flask_mail import Mail, Message
import os

login_manager = LoginManager(app)

CONTENT_FOLDER = os.getcwd() + "/instance/"

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
    return render_template("index.html.j2")

@app.route("/page/search")
@login_required
def search_page():
    return render_template("search.html.j2")

@app.route("/page/home")
@login_required
def home_page():
    result = db.session.execute(db.select(Content)).scalars().fetchmany(5)
    song_features = db.session.execute(db.select(FeaturedContent)).scalars().fetchmany(5)
    artist_features = db.session.execute(db.select(FeaturedArtists)).scalars().fetchmany(5)
    return render_template("home.html.j2", recent=result, song_features=song_features, artist_features=artist_features)

@app.route("/page/artist/<id>")
@login_required
def artist_page(id):
    artist = db.session.execute(db.select(Artist).filter(Artist.id == id)).fetchone()[0]
    print(artist)
    return render_template("artist.html.j2", artist=artist)

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

@app.route("/search/", methods=["POST", "GET"])
@login_required
def search():
    if request.method == "GET":
        pass
    elif request.method == "POST":
        query = request.json["searchInput"]

        if query == "":
            return ""

        artist = db.session.execute(db.select(Artist).where(Artist.name.like(f'%{query}%'))).scalars()
        content = db.session.execute(db.select(Content).where(Content.title.like(f'%{query}%'))).scalars()
        message = ""

        return render_template("search_result.html.j2", artists=artist, content=content, message=message)

def get_path(id):
    return CONTENT_FOLDER + "/content/" + str(id) + "/content.mp3"


@app.route("/artist/profile_picture/<id>")
@login_required 
def profile_picture(id):
    return send_file(CONTENT_FOLDER + "/artist/" + id + "/picture.png")

@app.route("/content/cover/<id>")
@login_required 
def contet_cover(id):
    return send_file(CONTENT_FOLDER + "/content/" + id + "/cover.png")

# @app.route("/content/stream/<id>")
# @login_required
# def content_stream(id):
#     file_path = get_path(id)
#     response = Response(stream_with_context(stream_audio(file_path)), mimetype="audio/mpeg")
#     return response
def stream_audio(file_path, start, length):
    with open(file_path, "rb") as audio_file:
        while True:
            audio_file.seek(start)
            data = audio_file.read(length)
            if not data:
                break
            yield data


@app.route("/content/stream/<id>")
@login_required
def content_stream(id):
    file_path = get_path(id)
    file_size = os.path.getsize(file_path)
    
    # Range header support for partial content
    range_header = request.headers.get('Range', None)
    if not range_header:
        response = Response(stream_with_context(stream_audio(file_path, 0, 1024)), mimetype="audio/mpeg")
        response.headers['Content-Length'] = 1024
    else:
        start, end = range_header.replace('bytes=', '').split('-')
        start = int(start)
        end = int(end) if end else file_size - 1
        length = end - start + 1
        response = Response(stream_with_context(stream_audio(file_path, start, length)), mimetype="audio/mpeg")
        response.headers['Content-Range'] = f'bytes {start}-{end}/{file_size}'
        response.headers['Content-Length'] = str(length)
        response.headers['Accept-Ranges'] = 'bytes'
        response.headers['Cache-Control'] = 'no-cache'
    response.status_code = 206

    return response

@app.route("/content/info/<id>")
@login_required 
def contet_info(id):
    song = db.session.execute(db.select(Content).filter(Content.id == id)).first()[0]
    return jsonify({"title": song.title, "artist": song.artist.name})

#
# Admin related endpoints
#

def allowed_picture(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png'}

def allowed_sound(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp3'}

@app.route("/admin/")
@login_required
def admin():
    if not current_user.is_admin():
        flash('You do not have permission to view this page.', 'danger')
        return redirect(url_for('index'))
    return render_template("admin.html.j2")

@app.route("/admin/artist/")
@login_required
def admin_artists():
    if not current_user.is_admin():
        flash('You do not have permission to view this page.', 'danger')
        return redirect(url_for('index'))

    artists = Artist.query.all()
    return render_template("admin_artists.html.j2", artists=artists)

@app.route("/admin/artist/add", methods=['POST'])
@login_required
def admin_add_artist():
    if not current_user.is_admin():
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('index'))

    artist_name = request.form['artistName']
    artist_picture = request.files['artistPicture']

    if artist_picture and allowed_picture(artist_picture.filename):
        # Create a new Artist
        new_artist = Artist(name=artist_name)
        db.session.add(new_artist)
        db.session.commit()

        # Save the profile picture with a unique filename

        os.mkdir(CONTENT_FOLDER + '/artist/' + str(new_artist.id))
        artist_picture_path = CONTENT_FOLDER + '/artist/' + str(new_artist.id) + '/picture.png'
        artist_picture.save(artist_picture_path)

        # Set the filename to the artist's profile image
        db.session.commit()

        flash(f'New artist {artist_name} added successfully.', 'success')
    else:
        flash('Invalid file format.', 'danger')        
    return redirect(url_for('admin_artists'))

@app.route("/admin/artist/remove/<id>", methods=['GET'])
@login_required
def remove_artist(id):
    if not current_user.is_admin():
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('index'))
    artist = db.get_or_404(Artist, id)
    db.session.delete(artist)
    db.session.commit()
    flash('Artist removed successfully.')
    return redirect(url_for('admin_artists'))


@app.route("/admin/artist/<int:artist_id>/songs", methods=['GET'])
@login_required
def admin_manage_artist_songs(artist_id):
    if not current_user.is_admin():
        flash('You do not have permission to view this page.', 'danger')
        return redirect(url_for('index'))

    artist = Artist.query.get_or_404(artist_id)
    songs = Content.query.filter_by(artist_id=artist.id).all()

    return render_template("admin_artist_songs.html.j2", artist=artist, songs=songs)

# In your Flask app file
@app.route("/admin/artist/<int:artist_id>/songs/add", methods=['POST'])
@login_required
def admin_add_song(artist_id):
    if not current_user.is_admin():
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        song_title = request.form['songTitle']
        song_audio_file = request.files['songFile']
        song_cover_file = request.files['coverFile']

        if song_audio_file and allowed_sound(song_audio_file.filename) and song_cover_file and allowed_picture(song_cover_file.filename):
            new_content = Content(title=song_title, artist_id=artist_id)
            db.session.add(new_content)
            db.session.commit()

            # Save the profile picture with a unique filename

            os.mkdir(CONTENT_FOLDER + '/content/' + str(new_content.id))
            content_sound_path = CONTENT_FOLDER + '/content/' + str(new_content.id) + '/content.mp3'
            content_cover_path = CONTENT_FOLDER + '/content/' + str(new_content.id) + '/cover.png'
            song_audio_file.save(content_sound_path)
            song_cover_file.save(content_cover_path)
            # Set the filename to the artist's profile image
            db.session.commit()

            flash(f'Song "{song_title}" successfully added to artist with ID #{artist_id}.', 'success')
            return redirect(url_for('admin_manage_artist_songs', artist_id=artist_id))
        else:
            flash(f'Song "{song_title}"')

    return redirect(url_for('admin_manage_artist_songs', artist_id=artist_id))


@app.route("/admin/artist/<int:artist_id>/songs/remove/<id>", methods=['GET'])
@login_required
def admin_remove_song(artist_id, id):
    if not current_user.is_admin():
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('index'))
    content = db.get_or_404(Content, id)
    db.session.delete(content)
    db.session.commit()
    return redirect(url_for('admin_manage_artist_songs', artist_id=artist_id))


@app.route("/admin/users")
@login_required
def admin_users():
    if not current_user.is_super_user():
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('index'))
    
    users = db.session.execute(db.select(User)).scalars()
    return render_template("admin_users.html.j2", users=users)

@app.route("/admin/users/invite", methods=["POST"])
@login_required
def invite_user():
    if not current_user.is_super_user():
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('index'))
    email = request.form["email"]
    invite = Invite(email)
    db.session.add(invite)
    db.session.commit()
    msg = Message(
         subject="Invite to VibeVault",
         recipients=[email],
         body=f"Click this link to verify your email: http://217.31.190.237/invite/{invite.email_verification_token}",
     )
    mail.send(msg)
    return redirect(url_for("admin_users"))

@app.route("/invite/<token>", methods=["GET", "POST"])
def accept_invite(token):
    print(token)
    invite = db.session.execute(db.select(Invite).where(Invite.email_verification_token == token)).scalar_one_or_none()
    if(invite != None):
        if request.method == "GET":
            return render_template("invite.html.j2", email=invite.email, action=url_for("accept_invite", token=token))
        elif request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            user = User(invite.email, username, password)
            db.session.add(user)
            db.session.commit()
            flash("Created an account, Enjoy!")
            return redirect(url_for("login_page"))
    return ""