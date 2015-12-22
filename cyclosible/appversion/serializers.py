from .models import AppVersion
from cyclosible.playbook.models import Playbook
from cyclosible.playbook.serializers import PlaybookSerializer
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist


class AppVersionSerializer(serializers.HyperlinkedModelSerializer):
    playbook = serializers.HyperlinkedRelatedField(
        read_only=False,
        lookup_field="name",
        view_name="playbook-detail")

    class Meta:
        model = AppVersion
        fields = ('url', 'playbook', 'application', 'version', 'env', 'deployed')

    def create(self, validated_data):
        print validated_data
        playbook_data = validated_data.get('playbook')
        try:
            playbook = Playbook.objects.get(name=playbook_data)
        except Playbook.DoesNotExist:
            raise ObjectDoesNotExist
        appversion = AppVersion.objects.create(playbook=playbook, **validated_data)
        return appversion

    def update(self, instance, validated_data):
        instance.application = validated_data.get('name', instance.name)
        instance.version = validated_data.get('only_tags', instance.only_tags)
        instance.env = validated_data.get('skip_tags', instance.skip_tags)
        instance.deployed = validated_data.get('extra_vars', instance.extra_vars)
        playbook_data = validated_data.get('playbook')
        try:
            playbook = Playbook.objects.get(name=playbook_data.get('name'))
            instance.playbook = playbook
        except Playbook.DoesNotExist:
            raise ObjectDoesNotExist
        return instance
