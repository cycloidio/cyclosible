from django.db import models
from cyclosible.playbook.models import Playbook


class AppVersion(models.Model):
    class Meta:
        app_label = 'appversion'

    ENV = (
        ('prod', 'prod'),
        ('preprod', 'preprod'),
        ('dev', 'dev'),
        ('infra', 'infra'),
    )

    application = models.CharField(max_length=100, null=False)
    version = models.CharField(max_length=128, null=False)
    env = models.CharField(max_length=10, choices=ENV, default='PROD')
    deployed = models.BooleanField(default=False)
    playbook = models.ForeignKey(Playbook)

    def __unicode__(self):
        return self.version
