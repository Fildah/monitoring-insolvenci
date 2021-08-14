from flask import Blueprint, render_template
from flask_migrate import upgrade

from monitoring_insolvenci.extensions import db
from monitoring_insolvenci.users.models import User

core = Blueprint('core', __name__)


# Obsluha zobrazeni domovske stranky
@core.route('/', methods=['GET'])
def index():
    return render_template('index.html', title='Monitoring insolvencí')


# Obsluha zobrazeni stranky o nas
@core.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title='O nás')


# CLI nasazeni apliakce a vytvoreni hlavniho administratora aplikace
@core.cli.command()
def deploy():
    upgrade()
    admin = User.query.filter_by(id=1).first()
    if not admin:
        admin = User('admin@admin.admin', 'Main', 'Admin', "12345pass")
        admin.toggle_admin()
        db.session.add(admin)
        db.session.commit()
