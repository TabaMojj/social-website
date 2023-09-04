from django.test import TestCase
from django.contrib.auth.models import User
from images.models import Image


class ImageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='testpass')
        Image.objects.create(user=user, title='Test Image', url='https://example.com/image.jpg')

    def test_title_max_length(self):
        image = Image.objects.get(id=1)
        max_length = image._meta.get_field('title').max_length
        self.assertEquals(max_length, 200)

    def test_get_absolute_url(self):
        image = Image.objects.get(id=1)
        self.assertEquals(image.get_absolute_url(), '/images/detail/1/test-image/')

    def test_slugify_on_save(self):
        image = Image.objects.create(user=User.objects.get(id=1), title='Another Test Image', url='https://example.com/another-image.jpg')
        self.assertEquals(image.slug, 'another-test-image')