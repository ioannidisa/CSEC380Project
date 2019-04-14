from django.test import TestCase
from django.contrib.auth.models import User


class LoginTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='zprobst',
                                        email='zap6135@rit.edu',
                                        password='test_password')
        user.save()

    def test_login_success(self):
        post = {
            'username': 'zprobst',
            'password': 'test_password',
        }

        # Make the request and expect to wind up on the profile page.
        response = self.client.post('/login/', post, follow=True)
        self.assertEqual(response.wsgi_request.path, '/profile')

    def test_wrong_password(self):
        post = {
            'username': 'zprobst',
            'password': 'test_password1',
        }

        # Make the request and expect to wind up on the profile page.
        response = self.client.post('/login/', post, follow=True)
        self.assertEqual(response.wsgi_request.path, '/login/')

    def test_wrong_username(self):
        post = {
            'username': 'zprobst1',
            'password': 'test_password',
        }

        # Make the request and expect to wind up on the profile page.
        response = self.client.post('/login/', post, follow=True)
        self.assertEqual(response.wsgi_request.path, '/login/')


class UserUploadDeleteTestCase(TestCase):
    pass