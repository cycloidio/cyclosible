# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playbook', '0006_auto_20151105_0618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playbook',
            name='subset',
            field=models.CharField(max_length=1024, blank=True, default=''),
        ),
    ]
