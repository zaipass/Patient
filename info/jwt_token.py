from django.conf import settings
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate

from info.models import Token

import jwt


def valiadate_token(request):
    token = request.headers.get('Jwt-Token', None)
    user_info = None
    detail = None
    types = 'error'

    if token is None:
        detail = "请求出现错误"
        return (detail, types)

    if token == 'null':
        detail = "身份信息过期, 请重新登录"
        return (detail, types)

    try:
        user_info = jwt.decode(token.encode(), settings.SECRET_KEY, algorithm='HS256')
    except jwt.exceptions.ExpiredSignatureError:
        detail = "身份信息过期, 请重新登录"
        return (detail, types)
    except Exception:
        detail = '请尝试重新登录'
        return (detail, types)

    if user_info:
        uinfo = user_info.get('data', None)
        try:
            user = authenticate(**uinfo)
            token_objects = Token.objects.filter(u_id=user.id).values('token')
        except TypeError:
            token_objects = None

        if not token_objects:
            return ('账号并未登录', types)

        if token in token_objects[0].values():
            types = 'correct'
            return (user, types)

    return ('请尝试重新登录', types)


def decorator_token(param=None):
    def func_token(func):
        def inner(request, *args, **kwargs):
            uinfo, tps = valiadate_token(request)

            if tps == 'error':
                return HttpResponseForbidden(uinfo)

            if param == 'logout':
                try:
                    Token.objects.filter(u_id=uinfo.id).delete()
                except Exception:
                    pass

            return func(request, *args, **kwargs)
        return inner
    return func_token
