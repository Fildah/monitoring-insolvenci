from flask import render_template, Blueprint
from flask_login import login_required, current_user

from monitoring_insolvenci.extensions import db
from monitoring_insolvenci.insolvencies.isir2 import Isir, fill_insolvency_with_isir
from monitoring_insolvenci.insolvencies.models import Insolvency
from monitoring_insolvenci.partners.models import Partner

insolvencies = Blueprint('insolvencies', __name__)


@insolvencies.get('/')
@login_required
def user_insolvencies():
    return render_template('user_insolvencies.html', title='Sledované insolvence partnerů', user=current_user)


@insolvencies.cli.command()
def update_insolvencies():
    isir = Isir()
    all_partners = Partner.query.all()
    for partner in all_partners:
        insolvencies_for_ico = isir.get_ico_insolvencies(partner.ico)
        for insolvency_data in insolvencies_for_ico:
            existing_insolvency = Insolvency.query.filter_by(ico=partner.ico, case=insolvency_data['bcVec'],
                                                             year=insolvency_data['rocnik']).first()
            if partner.insolvencies is not None:
                if existing_insolvency is None:
                    insolvency = fill_insolvency_with_isir(insolvency_data)
                    insolvency.partner.append(partner)
                    db.session.add(insolvency)
                else:
                    existing_insolvency.update_insolvency(insolvency_data)
        db.session.commit()
