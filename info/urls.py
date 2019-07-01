from django.urls import path
from info.views import (
    create_info,
    list_info,
    login,
    get_csrftoken,
    logout,
    index_page,
    manage_page,
    info_list_page,
    file_out,
)

urlpatterns = [
    # html-page
    path("", index_page),
    # manage-html-page
    path("manage/", manage_page),
    path("info-list/", info_list_page),
    # phone
    path("create-info/", create_info),
    path("token/", get_csrftoken),
    # user module
    path("login/", login),
    path("info/", list_info),
    path("logout/", logout),
    path("file-out/", file_out),
]
