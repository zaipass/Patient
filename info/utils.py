from django.http.request import QueryDict

from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _, ngettext

import pandas as pd


def output_file(filename="./demo.xlsx"):

    writer = pd.ExcelWriter(filename, engine="xlsxwriter")
    df = pd.DataFrame()
    df.to_excel(writer, sheet_name="信息表", index=False)
    wb = writer.book
    ws = writer.sheets["信息表"]

    return (ws, writer, wb)


def write_row(ws, row, col, value, style=None):
    if style:
        ws.write(row, col, value, style)

    ws.write(row, col, value, style)


def save_file(writer):
    writer.save()


def style_header(wb):
    # 1. 定义样式
    demo_style = {
        'bold': True,
        'fg_color': '#59c4b8',
        'font_size': 15,
        'align': 'center',
        'right': 1,
        'bottom': 1,
        'font_color': 'white',
    }
    style = wb.add_format(demo_style)

    return style


def query_to_dict(data):
    if type(data) == QueryDict:
        data = data.dict()
    return data


@deconstructible
class CodeUsernameValidator(validators.RegexValidator):
    regex = r"^[\w.+-]+$"
    message = _(
        "Enter a valid username. This value may contain only letters, "
        "numbers, and ./+/-/_ characters."
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
                    self.max_length,
                ),
                code="password_too_long",
                params={"max_length": self.max_length},
            )

    def get_help_text(self):
        return ngettext(
            "密码过长,需要小于%(max_length)d 位..", "密码过长,需要小于%(max_length)d 位.", self.max_length
        ) % {"max_length": self.max_length}
