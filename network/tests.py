from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse

from .models import NetworkNode


class NetworkNodeAPIPermissionsTest(APITestCase):

    def setUp(self):
        self.url = "/api/network-nodes/"

        # создаём завод (чтобы API не было пустым)
        NetworkNode.objects.create(
            name="Factory",
            node_type=0,
            email="f@test.com",
            country="USA",
            city="NY",
            street="Main",
            house_number="1"
        )

    def test_anonymous_user_cannot_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_non_staff_user_cannot_access(self):
        user = User.objects.create_user(username="user", password="12345", is_active=True)
        token = Token.objects.create(user=user)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)

    def test_inactive_staff_cannot_access(self):
        user = User.objects.create_user(
            username="staff",
            password="12345",
            is_active=False,
            is_staff=True
        )
        token = Token.objects.create(user=user)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 401)

    def test_active_staff_can_access(self):
        user = User.objects.create_user(username="admin", password="12345", is_active=True, is_staff=True)
        token = Token.objects.create(user=user)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
