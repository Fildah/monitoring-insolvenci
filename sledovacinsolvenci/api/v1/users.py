from flask import jsonify, request

from sledovacinsolvenci.api.v1 import api
from sledovacinsolvenci.extensions import api_auth


@api.get('/users')
@api_auth.login_required
def user_info():
    return jsonify({'data': api_auth.current_user().to_dict()})


@api.route('/users/<int:user_id>', methods=['DELETE'])
@api_auth.login_required
def user_edit(user_id):
    if user_id == api_auth.current_user().id:
        if request.method == 'DELETE':
            api_auth.current_user().deactivate()
            return jsonify({'data': 'Uživatel byl zneaktivněn!'})
