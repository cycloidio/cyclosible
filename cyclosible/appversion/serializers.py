from .models import AppVersion
from rest_framework import serializers


class AppVersionSerializer(serializers.HyperlinkedModelSerializer):
    playbook = serializers.HyperlinkedRelatedField(
        read_only=True,
        lookup_field="name",
        view_name="playbook-detail")

    class Meta:
        model = AppVersion
        fields = ('url', 'playbook', 'application', 'version', 'env', 'deployed')
