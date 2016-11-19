from flask import render_template, request, flash, redirect, url_for, g
from app import app, lm
from .forms import LoginForm, PostForm
from .model import User, Post
from flask_login import login_user, logout_user, current_user, login_required
import datetime

posts = [{'content': "Test post 1"}, {'content': "Test post 2"}]


@app.route('/index')
@app.route('/')
def index():
    return render_template('posts.html', posts=posts)


@login_required
@app.route('/writepost', methods=['GET', 'POST'])
def write_post():
    form = PostForm()
    if request.method == 'POST' and form.validate_on_submit():
        post = Post(username=g.user, timestamp=datetime.datetime.utcnow(), text=form.content.data)
    return render_template('writepost.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = app.config['USERS_COLLECTION'].find_one({"_id": form.username.data})

        remember = False
        if request.form.get('remember_me'):
            remember = True

        if user and User.validate_login(user['password'], form.password.data):
            user_obj = User(user['_id'], email=user['email'], full_name=user['full_name'])
            login_user(user_obj, remember=remember)
            flash("Logged in successfully", category='success')
            return redirect(request.args.get('next') or url_for('index'))
        flash("Wrong username or password", category='error')

    return render_template('login.html', title='login', form=form)


@app.route('/user/<name>')
@login_required
def user(name):
    user = app.config['USERS_COLLECTION'].find_one({'_id': name})
    if user is None:
        flash('Author {} not found'.format(name))
        return redirect('index')
    user = User(user['_id'], email=user['email'], full_name=user['full_name'])

    posts = [
        {'author': user, 'content': 'Test post #1'},
        {'author': user, 'content': 'Test post #2'}
             ]
    return render_template('user.html', user=user, posts=posts)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500



@app.before_request
def before_request():
    g.user = current_user


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@lm.user_loader
def load_user(username):
    u = app.config['USERS_COLLECTION'].find_one({"_id":username})
    if not u:
        return None
    return User(u['_id'], email=u['email'], full_name=u['full_name'])
