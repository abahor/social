import os
import random
import string
import datetime

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from myproject.users.date import date
# from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
import flask_whooshalchemy as wa

# from flask_static_compress import FlaskStaticCompress


app = Flask(__name__)
# ma = Marshmallow(app)
# compress = FlaskStaticCompress(app)
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LfjbcoUAAAAAEe1lrvl5rsSamajD_UISylnapZ2'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LfjbcoUAAAAAB05o1fHpTDU6p7X6vnaGWPONSTy'
# --------------- DATABASE
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'mykeyasdfghjklsdfghnjm'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://abahor:7X@9ydXxjvuZYPS@abahor.mysql.pythonanywhere-services.com/abahor$social'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['WHOOSH_BASE'] = 'whoosh'
app.config['WHOOSH_INDEX_PATH'] = 'whoo'

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10000 per day", "300 per hour"]
)
# app.config.update(
#     SESSION_COOKIE_SECURE=True,
#     SESSION_COOKIE_HTTPONLY=True,
#     SESSION_COOKIE_SAMESITE='Lax',
# )
app.config.update(
    debug=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='jousefgamal46@gmail.com',
    MAIL_PASSWORD='jousefgamal123456789'
)
mail = Mail(app)
# --------------- BUILD
db = SQLAlchemy(app)
Migrate(app, db)
# compress = FlaskStaticCompress(app)
# ---------------- LOGIN
login = LoginManager()
login.init_app(app)
login.login_view = 'users.login'

# ----------------- REGISTER_THE_BLUEPRINT
from myproject.users.views import users
from myproject.main.main import main  # , clever_function


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


@app.template_filter('re')
def r(value):
    dd = randomString()
    return dd


@app.template_filter('dat')
def dat(value):
    p = datetime.datetime.now() - datetime.timedelta(days=1)
    if value > p:
        return date(value)

    return value.strftime('%Y-%m-%d')


# app.jinja_env.globals.update(clever_function=clever_function)
app.register_blueprint(users)
app.register_blueprint(main)
# app.add_url_rule('/favicon.ico',redirect_to=url_for('static',filename='icons8-social-octopus-48.png'))
# d ='/ddd'
# print(d)