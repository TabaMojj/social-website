import os

from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model
from account.models import Profile, Contact


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            date_of_birth='1990-01-01'
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.date_of_birth, '1990-01-01')
        self.assertEqual(self.profile.photo, '')

    def test_profile_string_representation(self):
        self.assertEqual(str(self.profile), 'Profile of testuser')

    def test_profile_photo_upload(self):
        with open('./test.jpg', mode='w'): pass
        image_path = str(settings.MEDIA_ROOT / f'users/{self.user.username}/test.jpg')
        self.profile.photo = image_path
        self.profile.save()
        self.assertEqual(self.profile.photo.path, image_path)
        os.remove('./test.jpg')


class ContactModelTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password1'
        )
        self.user2 = get_user_model().objects.create_user(
            username='user2',
            email='user2@example.com',
            password='password2'
        )
        self.contact = Contact.objects.create(
            user_from=self.user1,
            user_to=self.user2
        )

    def test_contact_creation(self):
        self.assertEqual(self.contact.user_from, self.user1)
        self.assertEqual(self.contact.user_to, self.user2)

    def test_contact_string_representation(self):
        self.assertEqual(str(self.contact), 'user1 follows user2')

    def test_contact_ordering(self):
        contact2 = Contact.objects.create(
            user_from=self.user2,
            user_to=self.user1
        )
        contacts = Contact.objects.all()
        self.assertEqual(contacts[0], contact2)
        self.assertEqual(contacts[1], self.contact)


class UserModelTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password1'
        )
        self.user2 = get_user_model().objects.create_user(
            username='user2',
            email='user2@example.com',
            password='password2'
        )
        self.user1.following.add(self.user2)

    def test_user_following(self):
        self.assertTrue(self.user1.following.filter(username='user2').exists())
        self.assertFalse(self.user2.following.filter(username='user1').exists())
        self.assertTrue(self.user2.followers.filter(username='user1').exists())
