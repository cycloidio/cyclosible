from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class CoreTests(APITestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        # self.group = Group.objects.create(name="test_group_createuser")
        # self.group_url = '/api/v1/groups/%s/' % self.group.name
        self.admin = User.objects.create_superuser('admin', 'myemail@test.com', 'cyclosible')
        self.token = Token.objects.get(user__username='admin')

    def test_v1_create_group_not_authorized(self):
        """
        Ensure we can't create a new group object without auth.
        """
        url = '/api/v1/groups/'
        data = {'name': u'testgroup'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_v1_create_group(self):
        """
        Ensure we can create a new group object.
        """
        url = '/api/v1/groups/'
        data = {'name': u'testgroup'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), data.get('name'))

    def test_v1_create_user_not_authorized(self):
        """
        Ensure we can't create a new user object without auth.
        """
        url = '/api/v1/users/'
        data = {
            'username': u'testuser',
            'first_name': u'user',
            'last_name': u'test',
            'email': u'test@cycloid.io',
            'groups': [{'name': 'test_user_group'}]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_v1_create_user_authorized(self):
        """
        Ensure we can create a new user object.
        """
        url = '/api/v1/users/'
        data = {
            'username': u'testuser',
            'first_name': u'user',
            'last_name': u'test',
            'email': u'test@cycloid.io',
            'groups': [{'name': 'test_user_group'}]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('username'), data.get('username'))

    def test_v1_get_token(self):
        """
        Ensure we can get our token.
        """
        url = '/api-token-auth/'
        data = {
            'username': u'admin',
            'password': u'cyclosible',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('token'), self.token.key)
