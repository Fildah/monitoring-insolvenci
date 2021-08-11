import jwt

from monitorinsolvenci import config
from monitorinsolvenci.extensions import api_auth
from monitorinsolvenci.users.models import User


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
