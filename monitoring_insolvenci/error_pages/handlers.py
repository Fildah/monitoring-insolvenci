from flask import Blueprint, render_template, request, jsonify

error_pages = Blueprint('error_pages', __name__)


# Obsluha chyboveho kodu 403
@error_pages.app_errorhandler(403)
def error_403(error):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = {
            'error': 'Unauthorized.',
            'status_code': 403
        }
        return jsonify(response)
    return render_template('error_pages/general_error.html', error_message='403 Nepovolený přístup.'), 403


# Obsluha chyboveho kodu 404
@error_pages.app_errorhandler(404)
def error_404(error):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = {
            'error': 'Page not found.',
            'status_code': 404
        }
        return jsonify(response)
    return render_template('error_pages/general_error.html', error_message='404 Stránka nenalezena.'), 404


# Obsluha chyboveho kodu 500
@error_pages.app_errorhandler(500)
def error_500(error):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = {
            'error': 'Internal server error.',
            'status_code': 500
        }
        return jsonify(response)
    return render_template('error_pages/general_error.html', error_message='500 Problém na serveru.'), 500
