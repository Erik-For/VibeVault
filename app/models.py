from app import db
from flask_login import UserMixin
import bcrypt
from datetime import datetime
import secrets


class User(db.Model, UserMixin):
    __tablename = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(64))
    usertype = db.Column(db.Integer, default=0) # 0 default, 1 admin, 2 super user
    email = db.Column(db.String(100), unique=True)
    email_verified = db.Column(db.Boolean, default=False)
    email_verification_token = db.Column(db.String(32))

    def __init__(self, email, username, password):
        self.email = email.lower()
        self.username = username
        self.display_name = username
        self.password = bcrypt.hashpw(str(password).encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.email_verification_token = secrets.token_hex(32)[0:32-1]

    def is_admin(self):
        return (self.usertype >= 1)

    def is_super_user(self):
        return (self.usertype == 2)

    def check_password(self, password):
        return bcrypt.checkpw(str(password).encode('utf-8'), self.password.encode('utf-8'))
    
# Add ability to follow artists
    
class Invite(db.Model):
    __tablename__ = 'invites'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    email_verification_token = db.Column(db.String(32))

    def __init__(self, email):
        self.email = email
        self.email_verification_token = secrets.token_hex(32)[0:32-1]

class Artist(db.Model):
    __tablename__ = 'artists'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    contents = db.relationship('Content', backref='artist', lazy='dynamic')

class Content(db.Model):
    __tablename__ = 'contents'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    release_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)

class FeaturedContent(db.Model):
    __tablename__ = 'featured_content'
    
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('contents.id'), nullable=False)
    # Relationship to access the associated content
    content = db.relationship('Content', backref=db.backref('featured_content', uselist=False, cascade="all, delete"))

class FeaturedArtists(db.Model):
    __tablename__ = 'featured_artists'
    
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    # Relationship to access the associated content
    artist = db.relationship('Artist', backref=db.backref('featured_artists', uselist=False, cascade="all, delete"))