from flask import jsonify, request
from flask_login import login_required, current_user

from monitorinsolvenci.api.v1 import api
from monitorinsolvenci.extensions import api_auth
from monitorinsolvenci.extensions import db
from monitorinsolvenci.users.models import User


@api.get('/users')
@api_auth.login_required
def user_info():
    return jsonify({'data': api_auth.current_user().to_dict()})


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


@api.get('/users/ajax')
@login_required
def users_ajax():
    query = User.query.filter(User.id != 1).filter(User.id != current_user.id)
    all_user_partners = query.count()
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            User.id.like('%{}%'.format(search)),
            User.email.like('%{}%'.format(search)),
            User.first_name.like('%{}%'.format(search)),
            User.last_name.like('%{}%'.format(search))
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
