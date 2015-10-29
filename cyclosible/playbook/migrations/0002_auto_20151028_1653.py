# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playbook', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playbookrunhistory',
            name='date_finished',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
