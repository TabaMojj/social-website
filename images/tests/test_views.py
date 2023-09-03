import os

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from images.models import Image


class ImageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.image = Image.objects.create(user=self.user, title='Test Image', url='https://example.com/image.jpg')
        with open('./test.jpg', mode='w'):
            pass
        self.image.image = './test.jpg'
        self.image.save()

    def tearDown(self) -> None:
        User.objects.all().delete()
        Image.objects.all().delete()
        os.remove('./test.jpg')

    def test_image_create_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('images:create'), {
            'title': 'Test Image',
            'url': 'https://example.com/test-image.jpg',
            'description': 'New Image Description'
        })
        image = Image.objects.get(id=2)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, image.get_absolute_url())

    def test_image_detail_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('images:detail', args=[self.image.id, self.image.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'images/image/detail.html')
        self.assertEqual(response.context['image'], self.image)

    def test_image_like_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('images:like'), {
            'id': self.image.id,
            'action': 'like'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'ok')

    def test_image_list_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('images:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'images/image/list.html')
        self.assertContains(response, self.image.title)

    def test_image_ranking_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('images:ranking'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'images/image/ranking.html')
