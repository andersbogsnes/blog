from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms import StringField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class SignUpForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(max=64)])
    # password = PasswordField('password', validators=[DataRequired(), Length(max=50)])
    email = StringField('email', validators=[DataRequired(), Email(), Length(max=120)])
    first_name = StringField('first_name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('last_name', validators=[DataRequired(), Length(max=50)])


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('password', validators=[DataRequired(), Length(max=50)])
    remember_me = BooleanField('remember_me', default=False)


class PostForm(FlaskForm):
    content = TextAreaField('content', validators=[DataRequired()])


class UploadPostForm(FlaskForm):
    file = FileField('post', validators=[FileRequired(), FileAllowed(['md'], 'Only Markdown files!')])
    overwrite = BooleanField('overwrite', default=False)
