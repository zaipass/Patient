from django.http import JsonResponse
from django.shortcuts import render
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator

from django.contrib.auth import (
    authenticate,
    login as django_login,
    logout as django_logout,
)

from django.conf import settings
from django.middleware.csrf import get_token
from info.models import Info, Token
from info.error_dict import error_messages
from info.utils import query_to_dict, output_file, write_row, save_file
from info.jwt_token import decorator_token
from info.constants import xlsx_header

import jwt
import datetime
import json


def index_page(request):
    return render(request, "index.html")


def manage_page(request):
    return render(request, "back.html")


def info_list_page(request):
    return render(request, "list.html")


def get_csrftoken(request):
    token = get_token(request)
    response = JsonResponse({"detail": "登录成功"})
    response.set_cookie("csrftoken", token)
    return response


@decorator_token()
def file_out(request):
    username = request.user.username

    try:
        id_list = request.session.get(username)
    except KeyError:
        id_list = list()

    try:
        info_objects = Info.objects.filter(id__in=id_list)

        filepath = ''.join([settings.BASE_DIR, '/file_download/info.xlsx'])

        ws, writer = output_file(filename=filepath)

        header_column = dict()

        # write header
        current_row = 0
        current_col = 0
        for key, value in xlsx_header.items():

            write_row(ws, current_row, current_col, value)

            header_column.update({key: current_col})

            current_col += 1

        # writer content
        for obj in info_objects:
            current_row += 1

            for name, col_idx in header_column.items():

                write_row(ws, current_row, col_idx, obj.__dict__.get(name))

        save_file(writer)
    except Exception:
        return JsonResponse({"detail": "表格导出失败"}, status=400)

    return JsonResponse({"detail": "下载成功", "filename": 'info.xlsx'})


@decorator_token()
def list_info(request):
    page = request.GET.get("pageNumber", 1)

    info_objects = Info.objects.all().order_by("-create_time", "clinical_name")
    try:
        username = request.user.username
    except Exception:
        username = "user"

    try:
        id_list = []
        for i in info_objects.values("id"):
            id_list.append(i.get("id"))

        request.session["%s" % username] = id_list
    except Exception:
        pass

    paginator_object = Paginator(info_objects, settings.PER_PAGE_NUMS)

    total_numbers = paginator_object.count  # 总数
    # total_pages = paginator_object.num_pages  # 总页数
    # c = paginator_object.page_range  # 页数范围

    d = paginator_object.get_page(page)

    serializer = serialize("json", d.object_list, cls=DjangoJSONEncoder)

    info_list = json.loads(serializer)

    response_info = [info["fields"] for info in info_list]

    return JsonResponse(
        {"data": response_info, "total_numbers": total_numbers, "username": username}
    )


def create_info(request):
    data = query_to_dict(request.POST)

    if not data:
        return JsonResponse({"detail": "提交内容为空"}, status=400)

    if not any(list(data.values())):
        return JsonResponse({"detail": "提交内容为空"}, status=400)

    info = Info(**data)
    response_data = ""

    try:
        info.full_clean()
    except ValidationError as e:

        for k in e.message_dict.keys():
            if k in error_messages.keys():
                response_data += "%s<br />" % error_messages.get(k)

        return JsonResponse({"detail": response_data}, status=400)

    info.save()

    return JsonResponse({"detail": "提交信息成功"})


def login(request):
    data = query_to_dict(request.POST)
    now_time = datetime.datetime.now()
    expired_time = datetime.datetime.now() + datetime.timedelta(
        days=settings.EXPIRED_TIME
    )
    # expired_time = datetime.datetime.now() + datetime.timedelta(seconds=60)

    user = authenticate(**data)

    if user is None:
        return JsonResponse({"detail": "账号或密码错误"}, status=400)

    django_login(request, user)

    token = jwt.encode(
        {"data": data, "exp": expired_time, "iat": now_time},
        settings.SECRET_KEY,
        algorithm="HS256",
    )

    token_objs = Token.objects.filter(u_id=user.id)

    if token_objs:
        try:
            token_objs.update(token=token.decode("utf-8"))
        except Exception:
            return JsonResponse({"detail": "账号或密码错误"}, status=400)
    else:
        try:
            tk_object = Token(token=token.decode("utf-8"), u_id=user.id)
            tk_object.save()
        except Exception:
            return JsonResponse({"detail": "账号或密码错误"}, status=400)

    response = JsonResponse({"detail": "登录成功"})
    response.set_cookie("token", token.decode("utf-8"), expires=expired_time)
    return response


@decorator_token("logout")
def logout(request):
    try:
        django_logout(request)
    except Exception:
        return JsonResponse({"detail": "退出错误"}, status=400)

    return JsonResponse({"detail": "退出登录"})
