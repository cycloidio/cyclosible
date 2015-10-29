from django.contrib.auth.models import User, Group
from rest_framework import serializers
import logging
logger = logging.getLogger(__name__)


class GroupSerializerNoValidator(serializers.HyperlinkedModelSerializer):
    name = serializers.SlugField(validators=[])

    class Meta:
        model = Group
        lookup_field = 'name'
        fields = ('url', 'name')
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


class GroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group
        lookup_field = 'name'
        fields = ('url', 'name')
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


class UserSerializer(serializers.HyperlinkedModelSerializer):
    groups = GroupSerializerNoValidator(many=True, required=False)

    class Meta:
        model = User
        lookup_field = 'username'
        fields = ('url', 'first_name', 'last_name', 'username', 'email', 'groups')
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }

    def create(self, validated_data):
        groups_data = validated_data.pop('groups')
        user = User.objects.create(**validated_data)
        for group_data in groups_data:
            try:
                group = Group.objects.get(name=group_data.get('name'))
                group.user_set.add(user)
            except Group.DoesNotExist:
                group = Group.objects.create(**group_data)
                group.user_set.add(user)
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.groups.clear()
        groups_data = validated_data.get('groups')
        for group_data in groups_data:
            try:
                group = Group.objects.get(name=group_data.get('name'))
                group.user_set.add(instance)
            except Group.DoesNotExist:
                group = Group.objects.create(**group_data)
                group.user_set.add(instance)
        return instance
