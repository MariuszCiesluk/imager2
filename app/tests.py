import os
from io import BytesIO

from PIL import Image
from django.conf import settings
from django.http import Http404
from django.test import TestCase, RequestFactory
from django.core.files.uploadedfile import InMemoryUploadedFile

from app.constants import TEST_IMAGE
from app.forms import ImagerForm
from app.views import ImageView


class ImagerTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
        image.save(os.path.join(settings.MEDIA_ROOT, 'green.png'))

    def tearDown(self):
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, 'green.png'))
        except OSError:
            pass

    def test_not_existing_image(self):
        request_not_existing_image = self.factory.get('/imager/image/red/')

        with self.assertRaises(Http404):
            response = ImageView.as_view()(request_not_existing_image)

    def test_existing_image(self):
        request_existing_image = self.factory.get('/imager/image/green/')
        response = ImageView.as_view()(request_existing_image)
        self.assertEqual(response.status_code, 200)


class ImageUploadTest(TestCase):

    def setUp(self):
        self.image_blue = InMemoryUploadedFile(
            BytesIO(TEST_IMAGE),
            field_name='image',
            name='blue.png',
            content_type='image/png',
            size=(15, 15),
            charset='utf-8',
        )
        self.image_green = InMemoryUploadedFile(
            BytesIO(TEST_IMAGE),
            field_name='image',
            name='green.png',
            content_type='image/png',
            size=(5, 5),
            charset='utf-8',
        )
        img = Image.new('RGB', (10, 10))
        img.save(os.path.join(settings.MEDIA_ROOT, 'green.png'))

    def tearDown(self):
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, 'green.png'))
        except OSError:
            pass

        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, 'blue.png'))
        except OSError:
            pass

    def test_valid(self):
        form = ImagerForm(files={'image': self.image_green})
        self.assertEqual(form.is_valid(), True)

    def test_new_file(self):
        form = ImagerForm(files={'image': self.image_blue})
        if form.is_valid():
            form.save()
            uploaded_image = Image.open(os.path.join(settings.MEDIA_ROOT, 'blue.png'))
            self.assertEqual(uploaded_image.size, (15, 15))
        else:
            self.assertEqual(form.is_valid(), True)

    def test_existing_file(self):
        form = ImagerForm(files={'image': self.image_green})
        if form.is_valid():
            form.save()
            uploaded_image = Image.open(os.path.join(settings.MEDIA_ROOT, 'green.png'))
            self.assertEqual(uploaded_image.size, (5, 5))
        else:
            self.assertEqual(form.is_valid(), True)
