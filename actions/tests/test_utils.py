from unittest import mock

from actions.models import Action
from actions.utils import create_action
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from datetime import timedelta
from django.utils import timezone


class CreateActionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.content_type = ContentType.objects.create(model='dummy')

    def test_create_action_with_target(self):
        target = ContentType.objects.create()
        create_action(self.user, 'test', target=target)
        self.assertEqual(Action.objects.count(), 1)

    def test_create_action_without_target(self):
        create_action(self.user, 'test')
        self.assertEqual(Action.objects.count(), 1)

    def test_create_action_with_similar_actions(self):
        target = ContentType.objects.create()
        create_action(self.user, 'test', target=target)
        create_action(self.user, 'test', target=target)
        self.assertEqual(Action.objects.count(), 1)

    def test_create_action_with_similar_actions_time_limit(self):
        target = ContentType.objects.create()
        create_action(self.user, 'test', target=target)
        future_time = timezone.now() + timedelta(seconds=61)

        with mock.patch.object(timezone, 'now', return_value=future_time):
            create_action(self.user, 'test', target=target)
        self.assertEqual(Action.objects.count(), 2)
