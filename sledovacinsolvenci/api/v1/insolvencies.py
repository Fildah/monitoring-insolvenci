from flask import request
from flask_login import login_required, current_user

from sledovacinsolvenci.api.v1 import api
from sledovacinsolvenci.extensions import db
from sledovacinsolvenci.insolvency.models import Insolvency
from sledovacinsolvenci.partners.models import Partner


@api.get('/insolvencies', defaults={'partner_id': None})
@api.get('/insolvencies/<int:partner_id>')
@login_required
def insolvencies(partner_id):
    if partner_id is not None:
        query = Insolvency.query.filter(Insolvency.partner.any(Partner.id.in_([partner_id])))
    else:
        query = Insolvency.query.filter(Insolvency.partner.any(Partner.users.contains(current_user)))
    all_user_insolvencies = query.count()
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
    # sorting
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
