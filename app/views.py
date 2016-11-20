from flask import render_template, request, flash, redirect, url_for, g, Markup
from app import app, lm, db
from .forms import LoginForm, PostForm, UploadPostForm
from .model import User, Post
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
import markdown
import datetime
import os
from sqlalchemy.exc import IntegrityError


def convert_markdown(filename, get_header=False):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(filepath, mode='r', encoding='utf-8') as f:
        text = markdown.markdown(f.read())
    if get_header:
        teaser = text.split('<header>')[1].split('</header>')[0].strip()
        return Markup(teaser), Markup(text)
    return Markup(text)


def render_post(post):
    """Takes a Post object and converts to dict with rendered markdown"""
    teaser, text = convert_markdown(post.body, get_header=True)

    return {'user_id': post.author.id,
            'title': post.title,
            'author': post.author.full_name,
            'body': text,
            'teaser': teaser}


@app.route('/index')
@app.route('/')
def index():
    posts = Post.query.all()
    all_posts = [render_post(post) for post in posts]
    return render_template('posts.html', posts=all_posts)


@app.route('/about')
def about():
    return render_template('about.html')


@login_required
@app.route('/writepost', methods=['GET', 'POST'])
def write_post():
    form = PostForm()
    if request.method == 'POST' and form.validate_on_submit():
        pass
        # post = Post(username=g.user, timestamp=datetime.datetime.utcnow(), text=form.content.data)
    return render_template('writepost.html', form=form)


@login_required
@app.route('/upload', methods=['GET', 'POST'])
def upload_post():
    form = UploadPostForm()
    if request.method == 'POST' and form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        title = form.title.data

        if os.path.exists(filepath) and not form.overwrite.data:
            flash('A post with that name already exists! Upload aborted')
            return redirect(request.url)

        form.file.data.save(filepath)

        try:
            new_post = Post(user_id=g.user.id, title=title, body=filename, timestamp=datetime.datetime.utcnow())
            db.session.add(new_post)
            db.session.commit()
            flash('Post is live!')

        except IntegrityError as e:
            db.session.rollback()
            flash('A post with that name already exists, overwritten')
        redirect(url_for('index'))

    return render_template('upload.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        remember = False
        if request.form.get('remember_me'):
            remember = True

        if user and User.validate_login(user.password, form.password.data):
            login_user(user, remember=remember)
            flash("Logged in successfully", category='success')
            return redirect(request.args.get('next') or url_for('index'))
        flash("Wrong username or password", category='error')

    return render_template('login.html', title='login', form=form)


@app.route('/user/<int:user_id>')
@login_required
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        flash('Author {} not found'.format(user.full_name))
        return redirect('index')

    posts = user.posts
    return render_template('user.html', user=user, posts=posts)


@app.route('/post/<int:post_id>')
def get_post(post_id):
    post = Post.query.get(post_id)
    output = render_post(post)
    return render_template('post.html', post=output)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.before_request
def before_request():
    g.user = current_user


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
