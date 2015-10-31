from rest_framework import viewsets
from .models import Playbook, PlaybookRunHistory
from .serializers import (PlaybookSerializer, PlaybookRunHistorySerializer)
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.permissions import IsAdminUser
from .permissions import PlaybookPermissions
from .tasks import run_playbook as task_run_playbook
from .serializers import RunPlaybookSerializer


class PlaybookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows playbooks to be viewed or edited.
    """
    queryset = Playbook.objects.all()
    serializer_class = PlaybookSerializer
    lookup_field = 'name'
    permission_classes = (PlaybookPermissions,)
    filter_backends = (filters.DjangoObjectPermissionsFilter,)

    @detail_route(methods=['POST'], serializer_class=RunPlaybookSerializer)
    def run(self, request, name):
        """
        This function launch an ansible playbook in celery. The user must have the permission can_run_playbook
        :param request:
        :param name:
        :return:

        ---
        request_serializer: RunPlaybookSerializer
        response_serializer: RunPlaybookSerializer
        """

        if request.method == 'POST':
            playbook = self.get_object()
            if request.user.has_perm('playbook.can_run_playbook', playbook):
                serializer = RunPlaybookSerializer(data=request.data)
                if serializer.is_valid():
                    task = task_run_playbook.delay(playbook_name=playbook.name, user_name=request.user.username)
                    return Response(
                        {
                            'status': 'Playbook has been launched',
                            'task_id': task.id,
                            'websocket_url': 'ws://{server_name}:{server_port}/ws/{task_id}?subscribe-broadcast'.format(
                                server_name=request.META.get('SERVER_NAME'),
                                server_port=request.META.get('SERVER_PORT'),
                                task_id=task.id
                            ),
                        },
                        status=status.HTTP_201_CREATED
                    )
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status': 'You have not the permission to run this playbook'},
                                status=status.HTTP_403_FORBIDDEN)


class PlaybookRunHistoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows playbooks run history to be viewed only.
    """
    queryset = PlaybookRunHistory.objects.all()
    serializer_class = PlaybookRunHistorySerializer
    permission_classes = (IsAdminUser,)
