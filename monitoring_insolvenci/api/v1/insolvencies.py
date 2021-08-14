from flask import request, jsonify
from flask_login import login_required, current_user

from monitoring_insolvenci.api.v1 import api
from monitoring_insolvenci.extensions import api_auth
from monitoring_insolvenci.extensions import db
from monitoring_insolvenci.insolvencies.models import Insolvency
from monitoring_insolvenci.partners.models import Partner


# Obsluha vytvoreni seznamu vsech insolvenci partneru uzivatele
@api.get('/insolvencies')
@api_auth.login_required
def user_insolvencies():
    insolvencies = Insolvency.query.filter(Insolvency.partner.any(Partner.users.contains(api_auth.current_user())))
    return jsonify({'data': [insolvency.to_dict() for insolvency in insolvencies]})


# Obsluha vytvoreni slovniku s detailem insolvence
@api.get('/insolvencies/<int:insolvency_id>')
@api_auth.login_required
def insolvency_detail(insolvency_id):
    insolvency = Insolvency.query.filter_by(id=insolvency_id).first()
    return jsonify(insolvency.to_dict())


# Obsluha AJAXoveho pozadavku z DataTables na data insolvece/i sledovaneho/ych partnera/u uzivatele
@api.get('/insolvencies/ajax', defaults={'partner_id': None})
@api.get('/insolvencies/ajax/<int:partner_id>')
@login_required
def insolvencies_ajax(partner_id):
    # Rozliseni jestli se jedna o hromadny pohled (None) nebo konkretniho partnera (partner_id)
    if partner_id is not None:
        query = Insolvency.query.filter(Insolvency.partner.any(Partner.id.in_([partner_id])))
    else:
        query = Insolvency.query.filter(Insolvency.partner.any(Partner.users.contains(current_user)))
    all_user_insolvencies = query.count()
    # Omezeni dotazu podle hledani
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Insolvency.ico.like('%{}%'.format(search)),
            Insolvency.case.like('%{}%'.format(search)),
            Insolvency.state.like('%{}%'.format(search)),
            Insolvency.bankruptcy_start.like('%{}%'.format(search)),
            Insolvency.bankruptcy_end.like('%{}%'.format(search))
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
        if col_name not in ['ico', 'state', 'bankruptcy_start', 'bankruptcy_end']:
            col_name = 'name'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Insolvency, col_name)
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
        'data': [insolvency.to_dict() for insolvency in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': all_user_insolvencies,
        'draw': request.args.get('draw', type=int),
    }
