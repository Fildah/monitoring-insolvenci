from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_required, current_user

from sledovacinsolvenci.extensions import db
from sledovacinsolvenci.partners.forms import PartnerForm
from sledovacinsolvenci.partners.models import Partner

partners = Blueprint('partners', __name__)


@partners.get('/')
@login_required
def user_partners():
    page = request.args.get('page', 1, type=int)
    partners_for_user = Partner.query.filter(Partner.subscribers.contains(current_user)).paginate(page=page, per_page=5)
    return render_template('user_partners.html', title='Sledovani partneri', partners=partners_for_user,
                           user=current_user)


@partners.route('/create', methods=['GET', 'POST'])
@login_required
def create_partner():
    form = PartnerForm()
    if form.validate_on_submit():
        partner = Partner.query.filter_by(ico=form.ico.data).first()
        if partner:
            partner.subscribers.append(current_user)
            partner.active = True
        else:
            partner = Partner(ico=form.ico.data)
            partner.subscribers.append(current_user)
            db.session.add(partner)
        db.session.commit()
        flash('Partner vytvoren')
        return redirect(url_for('partners.partner_detail', partner_id=partner.id))
    return render_template('create_partner.html', title='Vytvoreni partnera', form=form)


@partners.get('/<int:partner_id>')
@login_required
def partner_detail(partner_id):
    partner = Partner.query.get_or_404(partner_id)
    if current_user not in partner.subscribers:
        abort(403)
    return render_template('partner_detail.html', title='Detail partnera: {}'.format(partner.ico), partner=partner)


@partners.post('/<int:partner_id>/delete')
@login_required
def delete_partner(partner_id):
    partner = Partner.query.get_or_404(partner_id)
    if current_user not in partner.subscribers:
        abort(403)
    print(current_user.id)
    partner.subscribers.remove(current_user)
    if len(partner.subscribers) == 0:
        partner.active = False
    db.session.commit()
    flash('Partner smazan')
    return redirect(url_for('core.index'))
