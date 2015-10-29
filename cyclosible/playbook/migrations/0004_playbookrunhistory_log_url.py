# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playbook', '0003_auto_20151028_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='playbookrunhistory',
            name='log_url',
            field=models.CharField(default=b'', max_length=1024, blank=True),
        ),
    ]
