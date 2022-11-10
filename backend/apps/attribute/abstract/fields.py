import datetime
import posixpath
import os

from django.db import models
from django.core.files.utils import validate_file_name
from django.core.files.storage import FileSystemStorage
from django.db.models import ImageField
from django.utils.translation import gettext_lazy as _

from project import settings
from slugify import slugify
import socket

class OverwriteStorage(FileSystemStorage):
    def check_file(self, name):
        file_dirname = '/'.join(name.split('/')[:-1])
        prefix = '/'.join(name.split('/')[-1:]).split('.')[0]
        dirname = os.path.join(settings.MEDIA_ROOT, file_dirname)

        for s in os.listdir(dirname):
            if os.path.splitext(s)[0] == prefix and os.path.isfile(os.path.join(dirname, s)):
                return os.path.join(dirname, s)
        return None

    def generate_filename(self, name):
        exist = self.check_file(name)
        if exist:
            os.remove(exist)
        return name


class AttributeImageField(ImageField):
    storage = OverwriteStorage

    def __init__(self, verbose_name=None, name=None, **kwargs):
        self.width_field, self.height_field = 100, 100
        kwargs['storage'] = self.storage
        super().__init__(verbose_name, name, **kwargs)

    def generate_filename(self, instance, filename):
        dirname = datetime.datetime.now().strftime(str(self.upload_to))
        filename = posixpath.join(dirname, filename)

        ext = filename.split('.')[-1]
        name = 'attributes/' + instance.get_slug
        filename = '.'.join([name, ext])

        filename = validate_file_name(filename, allow_relative_path=True)
        return self.storage.generate_filename(filename)

    @property
    def get_path(self):
        print(self.name)
        return socket.gethostname()


class AttributeGroupTypeAbstractField(models.CharField):
    TEXT = "text"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    FLOAT = "float"
    COLOR = "color"
    RANGE = "range"
    IMAGE = "image"

    TYPE_CHOICES = (
        (TEXT, _("Text")),
        (INTEGER, _("Integer")),
        (BOOLEAN, _("Boolean")),
        (FLOAT, _("Float")),
        (COLOR, _("Color")),
        (RANGE, _("Range")),
        (IMAGE, _("Image")),
    )

    class Meta:
        abstract = True


class AttributeGroupTypeField(AttributeGroupTypeAbstractField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = self.TYPE_CHOICES
        kwargs['default'] = self.TEXT
        kwargs['verbose_name'] = _("Type")
        super(AttributeGroupTypeField, self).__init__(*args, **kwargs)


class OptionGroupField(AttributeGroupTypeAbstractField):
    ATTRIBUTE = 'attribute'

    ATTRIBUTE_CHOICES = (
        (ATTRIBUTE, _("Attribute")),
    )

    TYPE_CHOICES = (
        *ATTRIBUTE_CHOICES,
        *AttributeGroupTypeAbstractField.TYPE_CHOICES,
    )

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = self.TYPE_CHOICES
        kwargs['default'] = self.ATTRIBUTE
        kwargs['verbose_name'] = _("Type")
        kwargs['max_length'] = 24
        super(OptionGroupField, self).__init__(*args, **kwargs)
