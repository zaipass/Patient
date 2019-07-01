from django.http.request import QueryDict

from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _, ngettext


def query_to_dict(data):
    if type(data) == QueryDict:
        data = data.dict()
    return data


@deconstructible
class CodeUsernameValidator(validators.RegexValidator):
    regex = r'^[\w.+-]+$'
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and ./+/-/_ characters.'
    )
    flags = 0


class MaxmumLengthValidator:
    """
    Validate whether the password is of a max length.
    """

    def __init__(self, max_length=16):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                ngettext(
                    "密码过长, 需要小于%(max_length)d 位.",
                    "密码过长, 需要小于%(max_length)d 位.",
                    self.max_length
                ),
                code='password_too_long',
                params={'max_length': self.max_length},
            )

    def get_help_text(self):
        return ngettext(
            "密码过长,需要小于%(max_length)d 位..",
            "密码过长,需要小于%(max_length)d 位.",
            self.max_length
        ) % {'max_length': self.max_length}
