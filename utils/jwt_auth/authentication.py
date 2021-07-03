"""
token 验证

Creator: Gao Junbin
Update: 2021-07-03
"""
from datetime import datetime
import jwt
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication, jwt_decode_handler
from calendar import timegm
from IcpSide import settings
from auth_user.models import Yonghu


def jwt_payload_handler(user_obj: Yonghu):
    iss_time = datetime.utcnow()
    payload = {
        "userid": user_obj.userid,
        "username": user_obj.username,
        'exp': iss_time + settings.JWT_AUTH.get("JWT_EXPIRATION_DELTA"),
    }
    # Include original issued at time for a brand new token,
    # to allow token refresh
    if settings.JWT_AUTH.get("JWT_ALLOW_REFRESH"):
        payload['orig_iat'] = timegm(
            iss_time.utctimetuple()
        )

    if settings.JWT_AUTH.get("JWT_AUDIENCE") is not None:
        payload['aud'] = settings.JWT_AUTH.get("JWT_AUDIENCE")

    if settings.JWT_AUTH.get("JWT_ISSUER") is not None:
        payload['iss'] = settings.JWT_AUTH.get("JWT_ISSUER")
    return payload


def parse_jwt_token(jwt_token):
    """验证jwt前缀是否合法"""
    token = jwt_token.split(" ")
    auth_header_prefix = settings.JWT_AUTH["JWT_AUTH_HEADER_PREFIX"].lower()
    if len(token) != 2 or token[0].lower() != auth_header_prefix:
        return None
    return token[1]


class JSONWebTokenAuthentication(BaseJSONWebTokenAuthentication):
    """JWT验证"""
    def get_authorization_header(self, request):
        try:
            auth = request.META.get('HTTP_AUTHORIZATION')
            return auth
        except AttributeError as e:
            return None

    def authenticate_credentials(self, payload):
        try:
            user_id = payload["userid"]
        except KeyError as e:
            return None
        user = Yonghu.objects.filter(userid=user_id)
        if user.count() == 0:
            return None
        return user[0]

    def authenticate(self, request):
        auth = self.get_authorization_header(request)
        if auth is None:
            return None
        # 自定义校验规则：auth_header_prefix token
        token = parse_jwt_token(auth)
        if token is None:
            return None
        try:
            # token => payload
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            return None
        except jwt.exceptions.DecodeError:
            return None
        # payload => user
        user = self.authenticate_credentials(payload)
        if user is None:
            return None
        return user
