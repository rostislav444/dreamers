import os
import posixpath

from django.core.files.storage import FileSystemStorage
from django.core.files.utils import validate_file_name
from django.db.models import FileField, ImageField
from django.utils.text import slugify
from unidecode import unidecode

from project import settings


class OverwriteStorage(FileSystemStorage):
    def check_dirs(self, dirname):
        path = ''
        for d in dirname.split('/'):
            path += d + '/'
            if not os.path.exists(path):
                os.mkdir(path)

    def check_file(self, name):
        file_dirname = '/'.join(name.split('/')[:-1])
        dirname = os.path.join(settings.MEDIA_ROOT, file_dirname)

        self.check_dirs(dirname)

        old_path = os.path.join(settings.MEDIA_ROOT, name)
        if os.path.exists(old_path):
            os.remove(old_path)
        return None

    def generate_filename(self, name):
        exist = self.check_file(name)
        if exist:
            os.remove(exist)
        return name


class CustomFileFieldAbstrct:
    storage = OverwriteStorage

    class Meta:
        abstract = True

    def __init__(self, verbose_name=None, name=None, ext=None, **kwargs):
        self.width_field, self.height_field = 100, 100
        kwargs['storage'] = self.storage
        super().__init__(verbose_name, name, **kwargs)

    def generate_filename(self, instance, filename):
        ext = filename.split('.')[-1]
        dirname = instance.__class__.__name__.lower()

        name = instance.get_name
        if hasattr(name, '__call__'):
            name = instance.get_name()

        new_filename = '.'.join([slugify(unidecode(name.lower())), ext])
        filename = posixpath.join(dirname, new_filename)
        filename = validate_file_name(filename, allow_relative_path=True)
        return self.storage.generate_filename(filename)


class CustomFileField(CustomFileFieldAbstrct, FileField):
    pass


class CustomImageField(CustomFileFieldAbstrct, ImageField):
    pass
