from flask import Blueprint

api = Blueprint('api_v1', __name__)

from monitoring_insolvenci.api.v1 import partners, insolvencies, auth, users, errors
