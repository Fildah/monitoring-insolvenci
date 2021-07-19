from flask import Blueprint, render_template

core = Blueprint('core', __name__)


@core.route('/')
def index():
    return render_template('index.html', title='Sledovac insolvenci')


@core.route('/about')
def about():
    return render_template('about.html', title='O nas')
