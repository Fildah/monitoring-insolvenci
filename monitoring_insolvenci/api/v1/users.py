from flask import jsonify, request
from flask_login import login_required, current_user

from monitoring_insolvenci.api.v1 import api
from monitoring_insolvenci.extensions import api_auth
from monitoring_insolvenci.extensions import db
from monitoring_insolvenci.users.models import User


# Obsluha vytvoreni slovniku s detailem uzivatele
@api.get('/users')
@api_auth.login_required
def user_info():
    return jsonify({'data': api_auth.current_user().to_dict()})


# Obsluha smazani uzivatele
@api.route('/users/<int:user_id>', methods=['DELETE'])
@api_auth.login_required
def user_edit(user_id):
    if user_id == api_auth.current_user().id:
        if request.method == 'DELETE':
            if current_user.admin:
                api_auth.current_user().toggle_active()
                return jsonify({'data': 'Uživatel byl zneaktivněn!'})
            else:
                return jsonify({'data': 'Uživatel je již neaktivní!'})


# Obsluha AJAXoveho pozadavku z DataTables na data administrace uzivatelu
@api.get('/users/ajax')
@login_required
def users_ajax():
    # Vyhledani vsech uzivatelu krome hlavniho admina a sebe sama
    query = User.query.filter(User.id != 1).filter(User.id != current_user.id)
    all_user_partners = query.count()
    # Omezeni dotazu podle hledani
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            User.id.like('%{}%'.format(search)),
            User.email.like('%{}%'.format(search)),
            User.first_name.like('%{}%'.format(search)),
            User.last_name.like('%{}%'.format(search))
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
        if col_name not in ['id', 'email', 'first_name', 'last_name', 'admin', 'active']:
            col_name = 'name'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(User, col_name)
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
        'data': [user.to_dict() for user in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': all_user_partners,
        'draw': request.args.get('draw', type=int),
    }
