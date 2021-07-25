from flask import render_template, Blueprint
from flask_login import login_required, current_user

from sledovacinsolvenci.extensions import db
from sledovacinsolvenci.insolvency.isir2 import Isir, fill_insolvency_with_isir
from sledovacinsolvenci.insolvency.models import Insolvency
from sledovacinsolvenci.partners.models import Partner

insolvencies = Blueprint('insolvencies', __name__)


@insolvencies.get('/')
@login_required
def user_insolvencies():
    return render_template('user_partners.html', title='Sledovaní partneři', user=current_user)


@insolvencies.cli.command()
def update_insolvencies():
    isir = Isir()
    all_partners = Partner.query.all()
    for partner in all_partners:
        insolvencies_for_ico = isir.get_ico_insolvencies(partner.ico)
        for insolvency_data in insolvencies_for_ico:
            existing_insolvencies = Insolvency.query.filter_by(ico=partner.ico, case=insolvency_data['bcVec']).first()
            if partner.insolvencies is not None and existing_insolvencies is None:
                insolvency = fill_insolvency_with_isir(insolvency_data)
                insolvency.partners.append(partner)
                db.session.add(insolvency)
        db.session.commit()
