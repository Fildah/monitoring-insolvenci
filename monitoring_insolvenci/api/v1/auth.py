import jwt

from monitoring_insolvenci import config
from monitoring_insolvenci.extensions import api_auth
from monitoring_insolvenci.users.models import User


# Obsluha overeni tokenu
@api_auth.verify_token
def verify_token(token):
    try:
        decoded_token = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
    except:
        return False
    if "user_id" in decoded_token:
        user = User.query.filter_by(id=decoded_token['user_id']).first()
        if user is not None and user.jwt_check(token) and user.active:
            return user
    return False
