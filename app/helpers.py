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
