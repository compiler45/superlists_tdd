from django.test import TestCase
from django.contrib import auth

from accounts.models import Token

# Create your tests here.

# stop 'last logged in' signal
auth.signals.user_logged_in.disconnect(auth.models.update_last_login)

User = auth.get_user_model()


class UserModelTest(TestCase):

    def test_user_is_valid_with_email_only(self):
        user = User(email='lain@b.com')
        user.full_clean()  # should not raise an error

    def test_email_is_primary_key(self):
        user = User(email='lain@b.com')
        self.assertEqual(user.pk, 'lain@b.com')

    def test_no_problem_with_auth_login(self):
        user = User.objects.create(email='lain@example.com')
        user.backend = ''
        request = self.client.request().wsgi_request
        auth.login(request, user)  # should not raise


class TokenModelTest(TestCase):

    def test_links_user_with_auto_generated_uid(self):
        #  ensure tokens for different users are unique
        token1 = Token.objects.create(email='lain@b.com')
        token2 = Token.objects.create(email='lain@b.com')
        self.assertNotEqual(token1.uid, token2.uid)
