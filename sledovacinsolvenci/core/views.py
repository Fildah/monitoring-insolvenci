from flask import Blueprint, render_template

core = Blueprint('core', __name__)


@core.route('/')
def index():
    return render_template('index.html')


@core.route('/about')
def about():
    return render_template('about.html')
