from django.utils.translation import gettext_lazy as _

error_messages = {
    'clinical_name': '诊所名称: 输入内容不可超过50位',
    'doc_name': '医生姓名: 输入内容不可超过20位',
    'doc_phone': '医生电话: 输入内容不可超过11位',
    'patient_name': '患者姓名: 输入内容不可超过20位',
    'sex_age': '年龄/性别: 输入内容不可超过6位',
    'patient_phone': '患者电话: 输入内容不可超过11位',
    'patient_detail': '患者描述: 输入内容不可超过300位',
}

# 自定义字段抛出的异常信息
field_error_msg = {
    'invalid_choice': _('Value %(value)r is not a valid choice.'),
    'null': _('This field cannot be null.'),
    'blank': _('内容不可为空'),
    'unique': _('此内容已经存在'),
    'unique_for_date': _("%(field_label)s must be unique for "
                         "%(date_field_label)s %(lookup_type)s."),
}
