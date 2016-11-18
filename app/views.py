from flask import render_template
from app import app

posts = [{'content': "Test post 1"}, {'content': "Test post 2"}]


@app.route('/')
def index():
    return render_template('index.html', posts=posts)