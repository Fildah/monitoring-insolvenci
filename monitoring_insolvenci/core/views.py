import os
from pathlib import Path

from flask import Blueprint, render_template
from flask_migrate import upgrade

from monitoring_insolvenci.extensions import db, COV
from monitoring_insolvenci.users.models import User

core = Blueprint('core', __name__)


@core.route('/', methods=['GET'])
def index():
    return render_template('index.html', title='Monitoring insolvencí')


@core.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title='O nás')


@core.cli.command()
def deploy():
    upgrade()
    admin = User.query.filter_by(id=1).first()
    if not admin:
        admin = User('admin@admin.admin', 'Main', 'Admin', "12345pass")
        admin.toggle_admin()
        db.session.add(admin)
        db.session.commit()


@core.cli.command()
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        covdir = os.path.join(Path(__file__).parents[2], 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
