from flask import jsonify


# Obsluha chyboveho kodu 400
def error_400(message):
    response = jsonify({
        'error': 'Bad request.',
        'message': message
    })
    response.status_code = 400
    return response


# Obsluha chyboveho kodu 401
def error_401(message):
    response = jsonify({
        'error': 'Unauthorized.',
        'message': message
    })
    response.status_code = 401
    return response


# Obsluha chyboveho kodu 405
def error_405(message):
    response = jsonify({
        'error': 'Method not allowed.',
        'message': message
    })
    response.status_code = 405
    return response
