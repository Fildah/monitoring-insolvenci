import datetime

from flask import render_template, Blueprint
from flask_login import login_required, current_user

from monitoring_insolvenci.emails.email_sender import send_email
from monitoring_insolvenci.extensions import db
from monitoring_insolvenci.insolvencies.isir2 import Isir, fill_insolvency_with_isir
from monitoring_insolvenci.insolvencies.models import Insolvency
from monitoring_insolvenci.partners.models import Partner
from monitoring_insolvenci.users.models import User

insolvencies = Blueprint('insolvencies', __name__)


# Obsluha zobrazeni vsech insolvenci sledovanych partneru uzivatele
@insolvencies.get('/')
@login_required
def user_insolvencies():
    return render_template('user_insolvencies.html', title='Sledované insolvence partnerů', user=current_user)


# CLI Aktualizace insolvenci
@insolvencies.cli.command()
def update_insolvencies():
    isir = Isir()
    insolvencies_for_notification = {}
    all_partners = Partner.query.all()
    for partner in all_partners:
        insolvencies_for_ico = isir.get_ico_insolvencies(partner.ico)
        if insolvencies_for_ico:
            for insolvency_data in insolvencies_for_ico:
                existing_insolvency = Insolvency.query.filter_by(ico=partner.ico, case=insolvency_data['bcVec'],
                                                                 year=insolvency_data['rocnik']).first()
                if existing_insolvency is None:
                    insolvency = fill_insolvency_with_isir(insolvency_data)
                    insolvency.partner.append(partner)
                    db.session.add(insolvency)
                    db.session.commit()
                    insolvencies_for_notification[insolvency.id] = {'time': insolvency.created,
                                                                    'type': 'new',
                                                                    'new_data': insolvency.to_dict()
                                                                    }
                else:
                    update_data = existing_insolvency.update_insolvency(insolvency_data)
                    if update_data is not False:
                        insolvencies_for_notification[existing_insolvency.id] = update_data
                        db.session.commit()
    users = User.query.all()
    for user in users:
        notification = {}
        for partner in user.partners:
            for insolvency in partner.insolvencies:
                if insolvency.id in insolvencies_for_notification:
                    if partner.id not in notification:
                        notification[partner.id] = {}
                        notification[partner.id]['name'] = partner.name
                        notification[partner.id]['ico'] = partner.ico
                        notification[partner.id]['insolvencies'] = {}
                    notification[partner.id]['insolvencies'][insolvency.id] = insolvencies_for_notification[
                        insolvency.id]
        if len(notification) != 0:
            send_email(user.email, 'Změny v insolvencích k {}'.format(datetime.date.today().strftime("%d.%m.%Y")),
                       'email/update_insolvencies',
                       title='Změny v insolvencích k {}'.format(datetime.date.today().strftime("%d.%m.%Y")), user=user,
                       notification=notification)
