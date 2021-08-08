from flask import jsonify


def error_400(message):
    response = jsonify({
        'error': 'Bad request.',
        'message': message
    })
    response.status_code = 400
    return response


def error_401(message):
    response = jsonify({
        'error': 'Unauthorized.',
        'message': message
    })
    response.status_code = 401
    return response


def error_403(message):
    response = jsonify({
        'error': 'Forbidden.',
        'message': message
    })
    response.status_code = 403
    return response


def error_405(message):
    response = jsonify({
        'error': 'Method not allowed.',
        'message': message
    })
    response.status_code = 405
    return response
