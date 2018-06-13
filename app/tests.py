import os
from io import BytesIO

from PIL import Image
from django.conf import settings
from django.test import TestCase, RequestFactory
from django.core.files.uploadedfile import InMemoryUploadedFile

from app.forms import ImagerForm
from app.helpers import get_image, handle_uploaded_file
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
        request_not_existing_image = self.factory.get('/image/not_a_colour/')

        response = ImageView.as_view()(request_not_existing_image)
        self.assertEqual(response.status_code, 404)

    def test_existing_image(self):
        request_existing_image = self.factory.get('/image/green/')
        print(request_existing_image.get_full_path())
        response = ImageView.as_view()(request_existing_image)
        self.assertEqual(response.status_code, 200)


class ImageUploadTest(TestCase):

    def setUp(self):
        image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
        image_io = BytesIO()
        image.save(image_io, 'png')
        image_io.seek(0)
        self.image_blue = InMemoryUploadedFile(
            image_io,
            field_name='image',
            name='blue.png',
            content_type='image/png',
            size=image_io.getbuffer().nbytes,
            charset='utf-8',
        )
        self.image_green = InMemoryUploadedFile(
            image_io,
            field_name='image',
            name='green.png',
            content_type='image/png',
            size=image_io.getbuffer().nbytes,
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
        form = ImagerForm(files={'image': self.image_green}, data={'title': 'green'})
        form.is_valid()
        self.assertEqual(form.is_valid(), True)

    def test_new_file(self):
        form = ImagerForm(files={'image': self.image_blue}, data={'title': 'blue'})
        if form.is_valid():
            title = (form.cleaned_data.get('title'))
            image = get_image(title)
            self.assertIsNone(image)
            handle_uploaded_file(form.cleaned_data.get('image'),
                                 '{}.{}'.format(title, form.cleaned_data.get('image').name.rsplit('.', 1)[1]))

            uploaded_image = Image.open(os.path.join(settings.MEDIA_ROOT, 'blue.png'))
            self.assertEqual(uploaded_image.size, (50, 50))
        else:
            self.assertEqual(form.is_valid(), True)

    def test_existing_file(self):
        form = ImagerForm(files={'image': self.image_green},data={'title': 'green'})
        if form.is_valid():
            title = (form.cleaned_data.get('title'))
            image = get_image(title)
            self.assertIsNotNone(image)
            handle_uploaded_file(form.cleaned_data.get('image'),
                                 '{}.{}'.format(title, image.rsplit('.', 1)[1]))

            uploaded_image = Image.open(os.path.join(settings.MEDIA_ROOT, 'green.png'))
            self.assertEqual(uploaded_image.size, (50, 50))
        else:
            self.assertEqual(form.is_valid(), True)
