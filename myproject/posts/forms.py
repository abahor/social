from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import *


class createPost(FlaskForm):
    text = TextAreaField('Text', render_kw={'placeholder': 'What do want to tell the world?'})
    title = StringField('Title', validators=[validators.DataRequired()], render_kw={'placeholder': 'Title'})
    media = FileField(validators=[FileAllowed(['jpg', 'png', 'gif', 'mp4', 'mkv'])])
    submit = SubmitField('Post')