from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from cyclosible.playbook.tasks import run_playbook as task_run_playbook
from cyclosible.playbook.models import Playbook
from guardian.shortcuts import assign_perm
import mock


class PlaybookTests(APITestCase):
    def setUp(self):
        # Create an authorized user
        self.user_authorized = User.objects.create_user('user_authorized_playbook', 'myemail@test.com', 'cyclosible')
        self.user_authorized_token = Token.objects.get(user__username='user_authorized_playbook')

        # Create an unauthorized user
        self.user_not_authorized = User.objects.create_user('user_not_authorized_playbook', 'myemail@test.com', 'cyclosible')
        self.user_not_authorized_token = Token.objects.get(user__username='user_not_authorized_playbook')

        # Create a group
        self.group = Group.objects.create(name="test_group_playbook")
        self.group_url = '/api/v1/groups/%s/' % self.group.name
        self.group.user_set.add(self.user_authorized)
        self.group.user_set.add(self.user_not_authorized)

        assign_perm('playbook.can_run_playbook', self.group)
        assign_perm('playbook.view_playbook', self.group)
        assign_perm('playbook.can_override_skip_tags', self.group)
        assign_perm('playbook.can_override_only_tags', self.group)

        # Create the playbook
        self.playbook = Playbook.objects.create(name="test_playbook", skip_tags="base", only_tags="deploy", group=self.group)

        # Create an admin
        self.admin = User.objects.create_superuser('admin_playbook', 'myemail@test.com', 'cyclosible')
        self.admin_token = Token.objects.get(user__username='admin_playbook')

        # Assign permissions for authorized user
        assign_perm('playbook.can_run_playbook', self.user_authorized, self.playbook)
        assign_perm('playbook.view_playbook', self.user_authorized, self.playbook)
        assign_perm('playbook.can_override_skip_tags', self.user_authorized, self.playbook)
        assign_perm('playbook.can_override_only_tags', self.user_authorized, self.playbook)

    def test_v1_create_playbook_not_authorized(self):
        """
        Ensure we can't create a new playbook object without auth.
        """
        url = '/api/v1/playbooks/'
        data = {
            'name': u'testplaybook',
            'only_tags': u'deploy',
            'skip_tags': u'base',
            'group': {'name': 'playbook_group'}
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_v1_create_playbook_forbidden(self):
        """
        Ensure we can't create a new playbook object with bad user.
        """
        url = '/api/v1/playbooks/'
        data = {
            'name': u'testplaybook',
            'only_tags': u'deploy',
            'skip_tags': u'base',
            'group': {'name': 'playbook_group'}
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_not_authorized_token.key)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_v1_create_playbook_group_not_exist(self):
        """
        Ensure we can create a new playbook object even if group does not exist
        """
        url = '/api/v1/playbooks/'
        data = {
            'name': u'testplaybook',
            'only_tags': u'deploy',
            'skip_tags': u'base',
            'group': {'name': 'test_group_not_exist_playbook'}
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), data.get('name'))

    def test_v1_create_playbook(self):
        """
        Ensure we can create a new playbook object.
        """
        url = '/api/v1/playbooks/'
        data = {
            'name': u'testplaybook',
            'only_tags': u'deploy',
            'skip_tags': u'base',
            'group': {'name': 'test_group_playbook'}
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), data.get('name'))

    def test_v1_admin_get_playbook(self):
        """
        Ensure we can get a playbook object with admin.
        """
        url = '/api/v1/playbooks/%s/' % self.playbook.name
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_v1_user_authorized_get_playbook(self):
        """
        Ensure we can get a playbook object with authorized user.
        """
        url = '/api/v1/playbooks/%s/' % self.playbook.name
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_authorized_token.key)
        response = self.client.get(url, format='json')
        print response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_v1_user_not_authorized_get_playbook(self):
        """
        Ensure we can't get a playbook object with an unauthorized user.
        """
        url = '/api/v1/playbooks/%s/' % self.playbook.name
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_not_authorized_token.key)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @mock.patch.object(task_run_playbook, 'delay')
    def test_v1_admin_run_playbook(self, mock_task_run_playbook_delay):
        """
        Ensure we can run a playbook object with admin.
        """
        url = '/api/v1/playbooks/%s/run/' % self.playbook.name
        data = {
            'only_tags': u'deploy',
            'skip_tags': u'base'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.post(url, data, format='json')
        mock_task_run_playbook_delay.assert_called_once_with(playbook_name=self.playbook.name, user_name=u'admin_playbook')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @mock.patch.object(task_run_playbook, 'delay')
    def test_v1_user_authorized_run_playbook(self, mock_task_run_playbook_delay):
        """
        Ensure we can run a playbook object with authorized user.
        """
        url = '/api/v1/playbooks/%s/run/' % self.playbook.name
        data = {
            'only_tags': u'deploy',
            'skip_tags': u'base'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_authorized_token.key)
        response = self.client.post(url, data, format='json')
        mock_task_run_playbook_delay.assert_called_once_with(playbook_name=self.playbook.name, user_name=u'user_authorized_playbook')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_v1_user_not_authorized_run_playbook(self):
        """
        Ensure we can't run a playbook object with an unauthorized user.
        """
        url = '/api/v1/playbooks/%s/run/' % self.playbook.name
        data = {
            'only_tags': u'deploy',
            'skip_tags': u'base'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_not_authorized_token.key)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
