from django.db import models
from django.contrib.auth.models import Group, User

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Playbook(models.Model):
    class Meta:
        app_label = 'playbook'
        permissions = (
            ("view_playbook", "Can view the playbook"),
            ("can_override_skip_tags", 'Can override skip_tags'),
            ("can_override_only_tags", 'Can override only_tags'),
            ("can_override_extra_vars", 'Can override extra_vars'),
            ("can_run_playbook", 'Can run the playbook')
        )

    name = models.CharField(max_length=100, unique=True, db_index=True)
    only_tags = models.CharField(max_length=1024, default='', blank=True)
    skip_tags = models.CharField(max_length=1024, default='', blank=True)
    extra_vars = models.CharField(max_length=1024, default='', blank=True)
    group = models.ForeignKey(Group, null=True)

    def __unicode__(self):
        return self.name


class PlaybookRunHistory(models.Model):
    class Meta:
        app_label = 'playbook'

    STATUS = (
        ('SUCCESS', 'Success'),
        ('RUNNING', 'Running'),
        ('FAILURE', 'Failure'),
    )

    playbook = models.ForeignKey(Playbook, db_index=True, related_name='history')
    date_launched = models.DateTimeField(blank=True)
    date_finished = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1024, default='RUNNING')
    task_id = models.CharField(max_length=1024, default='', blank=True)
    log_url = models.CharField(max_length=1024, default='', blank=True)
    launched_by = models.ForeignKey(User)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
