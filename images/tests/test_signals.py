from django.test import TestCase
from django.contrib.auth.models import User
from django.dispatch import Signal
from images.models import Image
from images.signals import users_like_changed


class UsersLikeChangedSignalTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass1')
        self.user2 = User.objects.create_user(username='user2', password='testpass2')
        self.image = Image.objects.create(user=self.user1, title='Test Image', url='https://example.com/image.jpg')

    def test_users_like_changed_signal(self):
        signal = Signal()
        signal.connect(users_like_changed, sender=Image.users_like.through)

        self.image.users_like.add(self.user1, self.user2)

        self.image.refresh_from_db()

        self.assertEqual(self.image.total_likes, 2)

        signal.disconnect(users_like_changed, sender=Image.users_like.through)
