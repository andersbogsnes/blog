from flask_wtf import Form
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class PostForm(Form):
    title = StringField('title', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])


class UploadPostForm(Form):
    title = StringField('title', validators=[DataRequired()])
    file = FileField('post', validators=[FileRequired(), FileAllowed(['md'], 'Only Markdown files!')])
    overwrite = BooleanField('overwrite', default=False)
