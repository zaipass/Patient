# Generated by Django 2.2.2 on 2019-06-27 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0007_auto_20190627_0442'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='u_id',
            field=models.IntegerField(default=1, help_text='对应用户', verbose_name='对应用户'),
            preserve_default=False,
        ),
    ]