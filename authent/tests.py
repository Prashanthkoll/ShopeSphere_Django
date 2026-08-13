from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class RegisterViewTests(TestCase):
    def test_register_page_loads(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_register_creates_user(self):
        response = self.client.post(reverse("register"), {
            "firstname": "Test",
            "lastname": "User",
            "name": "testuser",
            "email": "testuser@example.com",
            "password": "testpass123",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_register_rejects_duplicate_username(self):
        User.objects.create(username="dupeuser", email="a@example.com", password="x")
        response = self.client.post(reverse("register"), {
            "firstname": "Test",
            "lastname": "User",
            "name": "dupeuser",
            "email": "b@example.com",
            "password": "testpass123",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username="dupeuser").count(), 1)


class LoginViewTests(TestCase):
    def setUp(self):
        # authent's Login view compares plaintext passwords directly, so
        # this test creates the user the same (insecure) way instead of
        # via create_user(), to match actual app behaviour.
        self.user = User.objects.create(username="loginuser", password="testpass123")

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_login_succeeds_with_correct_credentials(self):
        response = self.client.post(reverse("login"), {
            "name": "loginuser",
            "password": "testpass123",
        })
        self.assertEqual(response.status_code, 302)

    def test_login_fails_with_wrong_password(self):
        response = self.client.post(reverse("login"), {
            "name": "loginuser",
            "password": "wrongpass",
        })
        self.assertEqual(response.status_code, 200)


class LogoutViewTests(TestCase):
    def test_logout_requires_login(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)