# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playbook', '0002_auto_20151028_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playbookrunhistory',
            name='playbook',
            field=models.ForeignKey(related_name='history', to='playbook.Playbook'),
        ),
    ]
