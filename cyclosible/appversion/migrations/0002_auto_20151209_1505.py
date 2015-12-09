# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appversion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appversion',
            name='application',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='appversion',
            name='version',
            field=models.CharField(max_length=128),
        ),
    ]
