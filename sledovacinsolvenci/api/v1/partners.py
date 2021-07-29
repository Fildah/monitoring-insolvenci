from flask import request
from flask_login import login_required, current_user

from sledovacinsolvenci.api.v1 import api
from sledovacinsolvenci.extensions import db
from sledovacinsolvenci.partners.models import Partner


@api.get('/partners')
@login_required
def partners():
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
