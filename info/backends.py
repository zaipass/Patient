from info.models import MyUser
from django.contrib.auth.backends import ModelBackend

import re


class UserLoginBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username:
            try:
                if '@' in username:
                    user = MyUser.objects.get(email=username)
                elif re.match(r'^1[3-9]\d{9}$', username):
                    user = MyUser.objects.get(phone=username)
                else:
                    user = MyUser.objects.get(username=username)
            except MyUser.DoesNotExist:
                return None
            else:
                if user.check_password(password):
                    return user
        else:
            return None
