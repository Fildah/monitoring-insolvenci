from flask import Blueprint, render_template
from flask_migrate import upgrade

core = Blueprint('core', __name__)


@core.route('/')
def index():
    return render_template('index.html', title='Sledovac insolvenci')


@core.route('/about')
def about():
    return render_template('about.html', title='O nas')


@core.cli.command()
def deploy():
    upgrade()
