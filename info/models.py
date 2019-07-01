from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UserManager
)
from info.utils import CodeUsernameValidator
from django.utils.translation import gettext_lazy as _

from django.core.mail import send_mail
from django.utils import timezone


class Info(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)

    clinical_name = models.CharField(verbose_name='诊所名称',
                                     help_text='诊所名称',
                                     blank=True,
                                     max_length=50)
    doc_name = models.CharField(max_length=20,
                                blank=True,
                                verbose_name='医生姓名',
                                help_text='医生姓名')
    doc_phone = models.CharField(max_length=11,
                                 blank=True,
                                 verbose_name='医生电话',
                                 help_text='医生电话')
    patient_name = models.CharField(max_length=20,
                                    blank=True,
                                    verbose_name='患者姓名',
                                    help_text='患者姓名')
    sex_age = models.CharField(max_length=6,
                               blank=True,
                               verbose_name='年龄/性别',
                               help_text='年龄/性别')
    patient_phone = models.CharField(max_length=11,
                                     blank=True,
                                     verbose_name='患者电话',
                                     help_text='患者电话')
    patient_detail = models.CharField(max_length=300,
                                      blank=True,
                                      verbose_name='患者描述',
                                      help_text='患者描述')

    def __str__(self):
        return self.patient_name

    class Meta:
        verbose_name = '信息'
        verbose_name_plural = verbose_name


class MyUser(AbstractBaseUser, PermissionsMixin):
    username_validator = CodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("该用户名已存在."),
        },
    )
    email = models.EmailField(_('邮箱地址'),
                              unique=True,
                              blank=True)
    phone = models.CharField(max_length=11,
                             unique=True,
                             null=True,
                             blank=True,
                             verbose_name='用户号码',
                             help_text='用户号码')
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('用户')
        verbose_name_plural = _('用户')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.username


class Token(models.Model):
    token = models.TextField(max_length=500,
                             verbose_name='token',
                             help_text='token')
    expired_time = models.CharField(max_length=30,
                                    verbose_name='过期时间',
                                    null=True,
                                    blank=True,
                                    help_text='过期时间')
    u_id = models.IntegerField(verbose_name='对应用户',
                               help_text='对应用户')
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = verbose_name
