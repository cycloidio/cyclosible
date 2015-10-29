# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Playbook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, db_index=True)),
                ('only_tags', models.CharField(default=b'', max_length=1024, blank=True)),
                ('skip_tags', models.CharField(default=b'', max_length=1024, blank=True)),
                ('group', models.ForeignKey(to='auth.Group', null=True)),
            ],
            options={
                'permissions': (('view_playbook', 'Can view the playbook'), ('can_override_skip_tags', 'Can override skip_tags'), ('can_override_only_tags', 'Can override only_tags'), ('can_run_playbook', 'Can run the playbook')),
            },
        ),
        migrations.CreateModel(
            name='PlaybookRunHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_launched', models.DateTimeField(blank=True)),
                ('date_finished', models.DateTimeField(blank=True)),
                ('status', models.CharField(default=b'RUNNING', max_length=1024)),
                ('task_id', models.CharField(default=b'', max_length=1024, blank=True)),
                ('launched_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('playbook', models.ForeignKey(to='playbook.Playbook')),
            ],
        ),
    ]
