from .models import Playbook, PlaybookRunHistory
from django.contrib.auth.models import Group
from rest_framework import serializers
from ..Cyclosible.serializers import GroupSerializerNoValidator
from django.core.exceptions import ObjectDoesNotExist


class PlaybookRunHistorySerializer(serializers.HyperlinkedModelSerializer):
    playbook = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    launched_by = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = PlaybookRunHistory
        fields = ('url', 'playbook', 'date_launched', 'date_finished', 'status', 'task_id', 'launched_by', 'log_url')


class FilteredHistorySerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.order_by('-date_launched')[:10]
        return super(FilteredHistorySerializer, self).to_representation(data)


class PlaybookRunHistoryLastSerializer(PlaybookRunHistorySerializer):
    class Meta:
        model = PlaybookRunHistory
        list_serializer_class = FilteredHistorySerializer


class PlaybookSerializer(serializers.HyperlinkedModelSerializer):
    group = GroupSerializerNoValidator(many=False, required=True)
    history = PlaybookRunHistoryLastSerializer(many=True, read_only=True)

    class Meta:
        model = Playbook
        fields = ('url', 'name', 'only_tags', 'skip_tags', 'extra_vars', 'subset', 'group', 'history')
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }

    def create(self, validated_data):
        group_data = validated_data.pop('group')
        try:
            group = Group.objects.get(name=group_data.get('name'))
        except Group.DoesNotExist:
            group = Group.objects.create(**group_data)
        playbook = Playbook.objects.create(group=group, **validated_data)
        return playbook

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.only_tags = validated_data.get('only_tags', instance.only_tags)
        instance.skip_tags = validated_data.get('skip_tags', instance.skip_tags)
        instance.extra_vars = validated_data.get('extra_vars', instance.skip_tags)
        instance.subset = validated_data.get('subset', instance.skip_tags)
        group_data = validated_data.get('group', {'name': instance.group.name})
        try:
            group = Group.objects.get(name=group_data.get('name'))
            instance.group = group
        except Group.DoesNotExist:
            raise ObjectDoesNotExist
        return instance


class RunPlaybookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Playbook
        fields = ('url', 'only_tags', 'skip_tags', 'extra_vars', 'subset')
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }
