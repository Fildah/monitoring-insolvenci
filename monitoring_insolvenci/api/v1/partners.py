from flask import request, jsonify
from flask_login import login_required, current_user

from monitoring_insolvenci.api.v1 import api
from monitoring_insolvenci.extensions import db, api_auth
from monitoring_insolvenci.partners.ares import get_ares_data, fill_partner_with_ares
from monitoring_insolvenci.partners.models import Partner


# Obsluha vytvoreni seznamu vsech partneru uzivatele, nebo vytvoreni noveho partnera
@api.route('/partners', methods=['GET', 'POST'])
@api_auth.login_required
def api_partners():
    if request.method == 'GET':
        partners = Partner.query.filter(Partner.users.contains(api_auth.current_user()))
        return jsonify({'data': [partner.to_dict() for partner in partners]})
    elif request.method == 'POST':
        ico = request.json.get('ico')
        if ico is not None or ico != '':
            partner = Partner.query.filter_by(ico=ico).first()
            if partner:
                if api_auth.current_user() not in partner.users:
                    partner.users.append(api_auth.current_user())
                    partner.active = True
            else:
                partner_ares = get_ares_data(ico)
                if partner_ares:
                    partner = fill_partner_with_ares(partner_ares)
                    partner.users.append(api_auth.current_user())
                    db.session.add(partner)
                else:
                    return jsonify({'data': 'Chyba v ICO'})
            db.session.commit()
            return jsonify({'data': partner.to_dict()})
        return jsonify({'data': 'Chyba v ICO'})


# Obsluha smazani partnera ze sledovani
@api.route('/partners/<int:partner_id>', methods=['DELETE'])
@api_auth.login_required
def api_partner_edit(partner_id):
    partner = Partner.query.filter_by(id=partner_id).first()
    if api_auth.current_user() in partner.users:
        if request.method == 'DELETE':
            partner.remove_user(api_auth.current_user())
            if len(partner.users) == 0:
                partner.toggle_active()
            return jsonify({'data': 'Partner byl smazán!'})


# Obsluha AJAXoveho pozadavku z DataTables na data sledovanych partneru uzivatele
@api.get('/partners/ajax')
@login_required
def partners_ajax():
    # Vyhledani sledovanych partneru uzivatele
    query = Partner.query.filter(Partner.users.contains(current_user))
    all_user_partners = query.count()
    # Omezeni dotazu podle hledani
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
    # Reseni razeni podle sloupcu
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
