import datetime

import markdown
from flask import render_template, request, flash, redirect, url_for, g, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError

from blog.extensions import lm, db
from blog.forms import LoginForm, UploadPostForm, SignUpForm, PostForm
from blog.model import User, Post


router = Blueprint('blog', __name__)


def convert_markdown(indata, text=False):
    """Helper function to convert markdown to html.
    :param indata: File object containging Markdown. If indata is a string, use text=True
    :param text: Default False. True if inputdata is a text string instead of filestream
    :returns title, html, original markdown
    """

    md = markdown.Markdown(extensions=['markdown.extensions.meta'])
    if not text:
        md_text = indata.read().decode('utf-8')
    else:
        md_text = indata
    text = md.convert(md_text)
    title = md.Meta['title'][0].strip()
    return title, text, md_text


@router.route('/index')
@router.route('/')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('posts.html', posts=posts)


@router.route('/about')
def about():
    return render_template('about.html')


@login_required
@router.route('/upload', methods=['GET', 'POST'])
def upload_post():
    form = UploadPostForm()
    if request.method == 'POST' and form.validate_on_submit():
        title, body, md_text = convert_markdown(form.file.data)

        try:
            new_post = Post(user_id=g.user.id, title=title, body=body, markdown=md_text)
            db.session.add(new_post)
            db.session.commit()
            flash('Post is live!')

        except IntegrityError as e:
            db.session.rollback()
            flash('A post with that name already exists, aborted!')
        redirect(url_for('blog.index'))

    return render_template('upload.html', form=form)


@router.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('blog.index'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        remember = False
        if request.form.get('remember_me'):
            remember = True

        if user and User.validate_login(user.password, form.password.data):
            login_user(user, remember=remember)
            flash("Logged in successfully", category='success')
            return redirect(request.args.get('next') or url_for('blog.index'))
        flash("Wrong username or password", category='error')

    return render_template('login.html', title='login', form=form)


@router.route('/user/<int:user_id>')
@login_required
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        flash('Author {} not found'.format(user_id))
        return redirect('index')

    return render_template('user.html', user=user, posts=user.posts)


@router.route('/post/<int:post_id>')
def get_post(post_id):
    post = Post.query.get(post_id)
    return render_template('post.html', post=post)


@login_required
@router.route('/edit_profile/<int:user_id>', methods=['POST', 'GET'])
def edit_profile(user_id):
    user = User.query.get(user_id)
    form = SignUpForm()
    if user:
        if not g.user.id == user.id:
            flash('Need to be logged in!')
            return redirect('blog.index')

        if request.method == 'POST':
            if request.form['submit'] == 'cancel':
                return redirect('index')
            user.username = form.username.data
            user.email = form.email.data
            user.full_name = ' '.join([form.first_name.data, form.last_name.data])
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('blog.edit_profile', user_id=user.id))

        form.username.data = user.username
        form.email.data = user.email
        first_name, last_name = user.full_name.split(" ")
        form.first_name.data = first_name
        form.last_name.data = last_name
        return render_template('editprofile.html', user=user, form=form)

    else:
        flash('User not found!', category='error')
        return redirect('index')


@login_required
@router.route('/edit_post/<int:post_id>', methods=['POST', 'GET'])
def edit_post(post_id):
    post = Post.query.get(post_id)
    form = PostForm()
    if not post.user_id == g.user.id:
        flash("Not logged in as the author")
        return redirect('blog.index')

    if request.method == 'POST':
        if request.form['submit'] == 'cancel':
            return redirect('blog.index')
        title, html, md_text = convert_markdown(form.content.data, text=True)
        post.markdown = form.content.data
        post.body = html
        post.timestamp = datetime.datetime.now()
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog.get_post', post_id=post.id))

    form.content.data = post.markdown
    return render_template('editpost.html', form=form, user=g.user)


@login_required
@router.route('/posts')
def posts():
    posts = g.user.posts
    return render_template('posts.html', posts=posts)


@router.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@router.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@router.before_request
def before_request():
    g.user = current_user


@router.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('blog.index'))


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
