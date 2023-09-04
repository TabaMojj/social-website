from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from actions.models import Action


class ActionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.content_type = ContentType.objects.create(model='dummy')
        self.action = Action.objects.create(user=self.user, verb='test', target_ct=self.content_type)

    def test_action_model_ordering(self):
        actions = Action.objects.all()
        self.assertEqual(actions[0], self.action)

    def test_action_model_indexes(self):
        indexes = Action._meta.indexes
        self.assertEqual(len(indexes), 2)
        self.assertEqual(indexes[0].fields, ['-created'])
        self.assertEqual(indexes[1].fields, ['target_ct', 'target_id'])
