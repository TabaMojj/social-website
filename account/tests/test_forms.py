from django.test import TestCase
from django.contrib.auth.models import User
from account.models import Profile
from account.forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm


class LoginFormTest(TestCase):
    def test_valid_form(self):
        form_data = {'username': 'testuser', 'password': 'testpassword'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {'username': '', 'password': ''}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())


class UserRegistrationFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'email': 'test@example.com',
            'password': 'testpassword',
            'password2': 'testpassword'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'email': 'test@example.com',
            'password': 'testpassword',
            'password2': 'differentpassword'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())


class UserEditFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com')
        User.objects.create(username='testuser2', email='test2@example.com')

    def test_valid_form(self):
        form_data = {'first_name': 'New', 'last_name': 'Name', 'email': 'new@example.com'}
        form = UserEditForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {'first_name': 'New', 'last_name': 'Name', 'email': 'test2@example.com'}
        form = UserEditForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())


class ProfileEditFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com')
        self.profile = Profile.objects.create(user=self.user, date_of_birth='1990-01-01')

    def test_valid_form(self):
        form_data = {'date_of_birth': '1990-01-02', 'photo': ''}
        form = ProfileEditForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {'date_of_birth': 'invalid-date', 'photo': ''}
        form = ProfileEditForm(data=form_data, instance=self.profile)
        self.assertFalse(form.is_valid())
