from io import BytesIO

from PIL import Image
from django.test import TestCase, RequestFactory


class ImagerTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
        self.existing_image = BytesIO(image.tostring())
        self.existing_image.name = 'green.png'
        self.existing_image.seek(0)
