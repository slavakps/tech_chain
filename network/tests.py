from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import NetworkNode


class NetworkNodeAPIPermissionsTest(APITestCase):

    def setUp(self):
        self.url = "/api/network-nodes/"
        NetworkNode.objects.create(
            name="Factory",
            email="f@test.com",
            country="USA",
            city="NY",
            street="Main",
            house_number="1"
        )

    def test_anonymous_user_cannot_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_inactive_user_cannot_access(self):
        user = User.objects.create_user(username="u", password="12345", is_active=False)
        token = Token.objects.create(user=user)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 401)

    def test_active_user_can_access(self):
        user = User.objects.create_user(username="u", password="12345", is_active=True)
        token = Token.objects.create(user=user)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
