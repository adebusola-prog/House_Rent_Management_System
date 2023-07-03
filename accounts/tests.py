from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.contrib.auth import get_user_model

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from .models import CustomUser


CREATE_ACCOUNT_URL = reverse('user_register')

def create_account(**params):
    return CustomUser.objects.create_user(**params)

class PublicAccountApiTests(TestCase):
    """Test the accounts API(public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_account_success(self):
        """Test creating account with valid payload is successful"""
        payload = {
            "email": "remi@gmail.com",
            "first_name": "remiiii",
            "last_name": "rem",
            "username": "Too",
            "password": "rulluyrulluy",
            "confirm_password": "rulluyrulluy",
            "signuptype": "H.O"
        }
        res = self.client.post(CREATE_ACCOUNT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        account = CustomUser.objects.get(email=res.data['email'])
        self.assertTrue(account.check_password(payload["password"]))
        self.assertNotIn('password', res.data)

    def test_account_exists(self):
        """Test create an account that already exists fails"""
        payload = {
            "email": "remi@gmail.com",
            "first_name": "remiiii",
            "last_name": "rem",
            "username": "Too",
            "password": "rulluyrulluy",
            "signuptype": "H.O"
        }
        create_account(**payload)
        res = self.client.post(CREATE_ACCOUNT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """ Test that password is more than 5 characters"""
        payload = {
            "email": "sammy@gmail.com",
            "password": "pw",
        }

        res = self.client.post(CREATE_ACCOUNT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        account_exists = CustomUser.objects.filter(email=payload.get("email"))
        self.assertFalse(account_exists)
