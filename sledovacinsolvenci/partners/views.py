from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_required, current_user

from sledovacinsolvenci.extensions import db
from sledovacinsolvenci.partners.ares import get_ares_data, fill_partner_with_ares
from sledovacinsolvenci.partners.forms import PartnerForm, ImportPartnerForm
from sledovacinsolvenci.partners.models import Partner

partners = Blueprint('partners', __name__)


@partners.get('/')
@login_required
def user_partners():
    return render_template('user_partners.html', title='Sledovaní partneři', user=current_user)


# TODO Presunout do API
@partners.get('/api')
@login_required
def api_partners():
    query = Partner.query.filter(Partner.users.contains(current_user))
    all_user_partners = query.count()
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Partner.ico.like('%{}%'.format(search)),
            Partner.dic.like('%{}%'.format(search)),
            Partner.name.like('%{}%'.format(search)),
            Partner.business_form.like('%{}%'.format(search)),
            Partner.state.like('%{}%'.format(search))
        ))
    total_filtered = query.count()
    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['ico', 'dic', 'name', 'state']:
            col_name = 'name'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Partner, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)
    return {
        'data': [partner.to_dict() for partner in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': all_user_partners,
        'draw': request.args.get('draw', type=int),
    }


@partners.route('/create', methods=['GET', 'POST'])
@login_required
def create_partner():
    form = PartnerForm()
    if form.validate_on_submit():
        partner = Partner.query.filter_by(ico=form.ico.data).first()
        if partner:
            if current_user not in partner.users:
                partner.users.append(current_user)
                partner.active = True
        else:
            partner_ares = get_ares_data(form.ico.data)
            if partner_ares:
                partner = fill_partner_with_ares(partner_ares)
                partner.users.append(current_user)
                db.session.add(partner)
            else:
                flash('Chyba IČO, nebo problém ve zpracování.', "warning")
                return render_template('create_partner.html', title='Vytvoření partnera', form=form)
        db.session.commit()
        flash('Partner vytvořen.', 'success')
        return redirect(url_for('partners.partner_detail', partner_id=partner.id))
    elif request.method != 'GET':
        flash('Chyba IČO, nebo problém ve zpracování.', "warning")
    return render_template('create_partner.html', title='Vytvoření partnera', form=form)


@partners.route('/import', methods=['GET', 'POST'])
@login_required
def import_partners():
    form = ImportPartnerForm()
    if form.validate_on_submit():
        file = form.file.data
        for line in file:
            line = line.strip().decode("utf-8")
            partner = Partner.query.filter_by(ico=line).first()
            if partner:
                if current_user not in partner.users:
                    partner.users.append(current_user)
                    partner.active = True
            else:
                partner_ares = get_ares_data(line)
                if partner_ares:
                    partner = fill_partner_with_ares(partner_ares)
                    partner.users.append(current_user)
                    db.session.add(partner)
            db.session.commit()
        return redirect(url_for('partners.user_partners'))
    return render_template('import_partners.html', title='Import partnerů', form=form)


@partners.get('/detail/', defaults={'partner_id': ''})
@partners.route('/detail/<int:partner_id>', methods=['GET', 'POST'])
@login_required
def partner_detail(partner_id):
    partner = Partner.query.get_or_404(partner_id)
    if current_user not in partner.users:
        abort(403)
    return render_template('partner_detail.html', title='Detail partnera: {}'.format(partner.ico), partner=partner)


@partners.post('/detail/<int:partner_id>/delete')
@login_required
def delete_partner(partner_id):
    partner = Partner.query.get_or_404(partner_id)
    if current_user not in partner.users:
        abort(403)
    print(current_user.id)
    partner.users.remove(current_user)
    if len(partner.users) == 0:
        partner.active = False
    db.session.commit()
    flash('Partner {} smazán.'.format(partner.name), 'success')
    return redirect(url_for('partners.user_partners'))
