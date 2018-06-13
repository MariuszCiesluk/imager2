import os

from django.conf import settings


def check_file(directory, prefix):
    """
    searching directory for file with prefix
    :param directory: place to check files
    :param prefix: name of file, without extension
    :return: file name with extension, False when it not exists
    """
    for s in os.listdir(directory):
        if os.path.splitext(s)[0] == prefix and os.path.isfile(os.path.join(directory, s)):
            return s
    return False


def get_image(file_name):
    """
    getting image file from MEDIA_ROOT for declared file_name prefix
    :param file_name:
    :return: path for image file; None when image do not exists
    """
    path = settings.MEDIA_ROOT
    founded_file = check_file(path, file_name)
    if founded_file:
        return os.path.join(settings.MEDIA_ROOT, founded_file)
    return None


def handle_uploaded_file(f, filename):
    """
    save uploaded file to destination
    :param f: file
    :param filename: name of file
    :return: None
    """
    with open(os.path.join(settings.MEDIA_ROOT, filename), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
