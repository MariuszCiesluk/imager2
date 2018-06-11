from io import BytesIO

from PIL import Image
from django.http import Http404
from django.test import TestCase, RequestFactory

from app.views import ImageView


class ImagerTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
        self.existing_image = BytesIO(image.tostring())
        self.existing_image.name = 'green.png'
        self.existing_image.seek(0)

    def not_existing_image(self):
        request_not_existing_image = self.factory.get('/imager/image/red/')

        with self.assertRaises(Http404):
            response = ImageView.as_view(request_not_existing_image)

    def existing_image(self):
        request_existing_image = self.factory.get('/imager/image/green/')
        response = ImageView.as_view(request_existing_image)
        self.assertEqual(response.status_code, 200)


# class ImagePathTest(TestCase):