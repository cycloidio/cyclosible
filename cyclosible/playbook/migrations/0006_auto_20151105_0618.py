# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playbook', '0005_auto_20151102_0655'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='playbook',
            options={'permissions': (('view_playbook', 'Can view the playbook'), ('can_override_skip_tags', 'Can override skip_tags'), ('can_override_only_tags', 'Can override only_tags'), ('can_override_extra_vars', 'Can override extra_vars'), ('can_override_subset', 'Can override subset'), ('can_run_playbook', 'Can run the playbook'))},
        ),
        migrations.AddField(
            model_name='playbook',
            name='subset',
            field=models.CharField(default=b'', max_length=1024, blank=True),
        ),
    ]
