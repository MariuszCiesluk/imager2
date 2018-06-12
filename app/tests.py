from io import BytesIO

from PIL import Image
from django.http import Http404
from django.test import TestCase, RequestFactory
from django.core.files.uploadedfile import InMemoryUploadedFile
from StringIO import StringIO

from app.constants import TEST_IMAGE
from app.forms import ImagerForm
from app.views import ImageView


class ImagerTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
        self.existing_image = BytesIO(image.tostring())
        self.existing_image.name = 'green.png'
        self.existing_image.seek(0)

    def test_not_existing_image(self):
        request_not_existing_image = self.factory.get('/imager/image/red/')

        with self.assertRaises(Http404):
            response = ImageView.as_view(request_not_existing_image)

    def test_existing_image(self):
        request_existing_image = self.factory.get('/imager/image/green/')
        response = ImageView.as_view(request_existing_image)
        self.assertEqual(response.status_code, 200)


class ImageUploadTest(TestCase):

    def setUp(self):
        self.image = InMemoryUploadedFile(
            BytesIO(TEST_IMAGE),
            field_name='tempfile',
            name='blue.png',
            content_type='image/png',
            size=len(TEST_IMAGE),
            charset='utf-8',
        )

    def test_valid(self):
        form = ImagerForm(files={'image': self.image})
        self.assertEqual(form.is_valid(), True)
