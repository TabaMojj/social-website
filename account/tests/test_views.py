from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from account.models import Contact


class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_dashboard_view(self):
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/dashboard.html')


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_view(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register.html')

    def test_register_view_post(self):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'password2': 'newpassword',
            'first_name': 'first_name',
            'email': 'testemail@gmail.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register_done.html')
        self.assertTrue(User.objects.filter(username='newuser').exists())


class UserFollowViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.client.login(username='user1', password='password1')

    def test_user_follow_view(self):
        url = reverse('user_follow')
        data = {
            'id': self.user2.id,
            'action': 'follow'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.filter(user_from=self.user1, user_to=self.user2).count(), 1)

    def test_user_unfollow_view(self):
        Contact.objects.create(user_from=self.user1, user_to=self.user2)
        url = reverse('user_follow')
        data = {
            'id': self.user2.id,
            'action': 'unfollow'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.filter(user_from=self.user1, user_to=self.user2).count(), 0)
