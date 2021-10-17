from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import *
from wtforms.validators import DataRequired, EqualTo, Email


class searchForm(FlaskForm):
    searchText = StringField('Search', validators=[DataRequired()], render_kw={'placeholder': 'Search'})
    submit = SubmitField()


class updatePOSTForm(FlaskForm):
    title = StringField(validators=[DataRequired()], render_kw={'placeholder': 'title'})
    text = TextAreaField(render_kw={'placeholder': 'Text'})
    media = FileField(validators=[FileAllowed(['jpg', 'png', 'gif', 'mp4', 'mkv'])])
    submit = SubmitField('update')