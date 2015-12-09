# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playbook', '0007_auto_20151209_1444'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('application', models.CharField(max_length=100, unique=True)),
                ('version', models.CharField(max_length=128, default='')),
                ('env', models.CharField(max_length=10, choices=[('PROD', 'prod'), ('PREPROD', 'preprod'), ('DEV', 'dev'), ('INFRA', 'infra')], default='PROD')),
                ('deployed', models.BooleanField(default=False)),
                ('playbook', models.ForeignKey(to='playbook.Playbook')),
            ],
        ),
    ]
