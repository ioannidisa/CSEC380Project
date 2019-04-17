from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, LiveServerTestCase
from django.contrib.auth.models import User

from bs4 import BeautifulSoup

from .models import Video


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


class VideoUploadTestCase(TestCase):
    def test_actual_file(self):
        # First create a user for the test
        user = User.objects.create(username='testuser')
        user.set_password('123456')
        user.save()

        # Second log them in.
        self.client.login(username='testuser', password='123456')

        video = SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")
        response = self.client.post('/upload', {
            'name': 'file test',
            'desc': 'This is a file test',
            'file': video
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        vid = Video.objects.all().order_by("-id")[0]

        response = self.client.post('/delete', {
            'id': vid.id,
        }, follow=True)

        self.assertEqual(response.redirect_chain[0], ('/', 302))
        self.assertEqual(response.status_code, 200)

    def test_from_url(self):
        # First create a user for the test
        user = User.objects.create(username='testuser')
        user.set_password('123456')
        user.save()

        # Second log them in.
        self.client.login(username='testuser', password='123456')

        response = self.client.post('/upload', {
            'name': 'file test',
            'desc': 'This is a file test',
            'url': 'https://player.vimeo.com/external/290426949.hd.mp4?s=1e0af236aed4122ecb410ed8fcb3f24b08f1afc8&profile_id=175&oauth2_token_id=57447761&download=1t'
        }, follow=True)

        vid = Video.objects.all().order_by("-id")[0]

        response = self.client.post('/delete', {
            'id': vid.id,
        }, follow=True)

        self.assertEqual(response.redirect_chain[0], ('/', 302))
        self.assertEqual(response.status_code, 200)


class SSRFTestCase(LiveServerTestCase):
    def test_ssrf(self):
        # First create a user for the test
        user = User.objects.create(username='testuser')
        user.set_password('123456')
        user.save()

        # Second log them in.
        self.client.login(username='testuser', password='123456')

        # First upload with the URL /etc/passwd
        response = self.client.post('/upload', {
            'name': 'ssrf',
            'desc': 'This is an ssrf test',
            'url': 'file:///etc/passwd'
        }, follow=True)

        soup = BeautifulSoup(response.content, features='html.parser')
        file = soup.find_all('source')[0]['src']
        self.assertTrue(file.endswith('passwd'))


class ClassicSQLInjection(TestCase):
    def test_sql_injection(self):
        # First lets creat a bunch od data
        user = User.objects.create(username='testuser')
        user.set_password('123456')
        user.save()

        video_one = Video.objects.create(name='Test 1', desc='This is a test', views=0, owner=user)
        video_two = Video.objects.create(name='Test 2', desc='This is a test', views=0, owner=user)
        video_three = Video.objects.create(name='Test 3', desc='This is a test', views=0, owner=user)

        self.assertEqual(3, len(Video.objects.all()))

        # Do a regular search
        self.client.get('/search?q=Test')

        # Now, we need to perform the SQL injection
        self.client.get('/search?q=%27%3B+delete+from+app_video+--')

        self.assertEqual(0, len(Video.objects.all()))
