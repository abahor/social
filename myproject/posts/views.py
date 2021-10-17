from flask import Blueprint, render_template, redirect, request,url_for
from myproject import db
from myproject.models import Posts, comments, Users
from myproject.main.forms import searchForm
from myproject.posts.forms import createPost
from flask_login import login_required, login_user, current_user

posts = Blueprint('posts', __name__, template_folder='temp')


# @posts.route('/index')
