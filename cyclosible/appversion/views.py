from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from .models import AppVersion
from .serializers import (AppVersionSerializer)


class AppVersionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows interact with applications versions.
    """
    queryset = AppVersion.objects.all()
    serializer_class = AppVersionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('env', 'playbook', 'application', 'version')
    permission_classes = (permissions.IsAuthenticated,)
