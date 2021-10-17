from myproject import db, login, app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from myproject import wa


# from myproject import ma


@login.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    profile_pic = db.Column(db.String(64), default='/static/pics/default.jpg', nullable=False)
    post = db.relationship('Posts', backref='author', lazy='dynamic')
    user_comments = db.relationship('comments', backref='user_comments', lazy='joined')

    def __init__(self, email, username, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, field):
        return check_password_hash(self.password, field)


class Posts(db.Model):
    __tabelname__ = 'posts'
    __searchable__ = ['title', 'text']

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.Text)
    images = db.Column(db.Integer, db.ForeignKey('media.id'), default=1)
    title = db.Column(db.Text, nullable=False)
    m = db.Column(db.String(1))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comments_on_the_post = db.relationship('comments', backref='comments_on', lazy=True)
    media = db.relationship('media', backref='media_content', uselist=False)

    def __init__(self, text, title, user_id, images=None, m=None):
        self.text = text
        self.title = title
        self.user_id = user_id
        self.images = images
        self.m = m


class media(db.Model):
    __tabelname__ = 'media'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    media_url = db.Column(db.Text)

    def __init__(self, media_url):
        self.media_url = media_url


class comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    text = db.Column(db.Text)
    media = db.Column(db.Text)

    def __init__(self, text, media, user_id, post_id):
        self.text = text
        self.media = media
        self.user_id = user_id
        self.post_id = post_id


# class Usersshema(ma.ModelSchema):
#     class Meta:
#         model = Users
#
#
# class Postsshema(ma.ModelSchema):
#     class Meta:
#         model = Posts
#
#
# class Commentsshema(ma.ModelSchema):
#     class Meta:
#         model = comments
wa.search_index(app=app, model=Posts)