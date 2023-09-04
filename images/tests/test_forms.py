from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from images.form import ImageCreateForm


class ImageCreateFormTest(TestCase):
    def test_clean_url_valid_extension(self):
        form_data = {
            'title': 'Test Image',
            'url': 'https://example.com/image.jpg',
            'description': 'Test Description',
        }
        form = ImageCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_clean_url_invalid_extension(self):
        form_data = {
            'title': 'Test Image',
            'url': 'https://example.com/image.txt',
            'description': 'Test Description',
        }
        form = ImageCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('url', form.errors)

    def test_save_method(self):
        form_data = {
            'title': 'Test Image',
            'url': 'https://example.com/image.jpg',
            'description': 'Test Description',
        }
        image_file = SimpleUploadedFile('image.jpg', b'file_content', content_type='image/jpeg')
        form = ImageCreateForm(data=form_data, files={'image': image_file})
        self.assertTrue(form.is_valid())

        image = form.save(commit=False)
        self.assertEqual(image.title, 'Test Image')
        self.assertEqual(image.description, 'Test Description')
