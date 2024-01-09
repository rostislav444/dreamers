import os
import random
import string
from io import BytesIO

from PIL import Image
from django import forms
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.forms.widgets import FileInput

from project.settings import MEDIA_ROOT, FILE_STORAGE


class DeleteMethods:
    def get_old_file(self, model_instance):
        old_instance = model_instance.__class__.objects.filter(pk=model_instance.pk).first()
        if old_instance:
            return getattr(old_instance, self.name)
        return None

    def delete(self, instance, using=None, keep_parents=False):
        self.delete_file(instance)
        self.delete_empty_app_directories(instance)
        self.delete_thumbnails(instance)

    def delete_thumbnails(self, instance):
        thumbnails_field_name = self.name + '_thumbnails'
        if hasattr(instance, thumbnails_field_name):
            for filename in getattr(instance, thumbnails_field_name).values():
                self.storage.delete(filename)

    def delete_file(self, instance):
        file_to_delete = getattr(instance, self.name, None)
        if file_to_delete:
            self.storage.delete(file_to_delete.name)
            self.delete_thumbnails(instance)

    def delete_empty_app_directories(self, instance):
        app_media_path = os.path.join(MEDIA_ROOT, instance.__class__._meta.app_label)
        self._recursive_remove_empty_directories(app_media_path)

    def _recursive_remove_empty_directories(self, directory):
        if not os.path.exists(directory):
            return

        for root, dirs, files in os.walk(directory, topdown=False):
            if not dirs and not files:
                self.storage.delete(root)


class FileNaming:
    def generate_filename(self, instance, filename):
        new_filename = self.get_dirs(instance, filename)
        return new_filename

    def generate_random_name(self, length=8):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    @staticmethod
    def get_possible_names(instance):
        for field in ['slug', 'code', 'name', 'art', 'article', 'title']:
            if hasattr(instance, field):
                name = getattr(instance, field)
                return name
        return None

    def get_foreignkey_name(self, instance):
        for field in instance.__class__._meta.get_fields():
            if isinstance(field, models.ForeignKey):
                fk_instance = getattr(instance, field.name)
                if fk_instance:
                    return str(fk_instance.pk)
        return None

    def get_instance_name(self, instance):
        name = self.get_possible_names(instance)
        return name if name else self.generate_random_name(6)

    def get_name(self, field_name, instance, filename):
        ext = filename.split('.')[-1]
        instance_name = self.get_instance_name(instance)
        return f'{field_name}-{instance_name}.{ext}'

    def construct_filename(self, instance, filename):
        return self.get_name(self.name.lower(), instance, filename)

    @staticmethod
    def check_dirs_exist(path_parts):
        directory = os.path.join(*path_parts[:-1])
        if not os.path.exists(directory):
            os.makedirs(directory)

    def get_dirs(self, instance, filename):
        parts = [
            instance.__class__._meta.app_label,
            instance.__class__.__name__.lower(),
        ]

        parent_dir_name = self.get_foreignkey_name(instance)
        if parent_dir_name:
            parts.append(parent_dir_name)

        self.check_dirs_exist(parts)
        parts.append(self.construct_filename(instance, filename))
        return os.path.join(*parts)


class DeletableMediaField(FileNaming, DeleteMethods, models.FileField):
    valid_extensions = []
    storage = FILE_STORAGE

    class Meta:
        abstract = True

    def __init__(self, *args, get_parent=None, **kwargs):
        self.get_parent = get_parent
        kwargs['storage'] = self.storage
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        file_instance = getattr(model_instance, self.name)
        if not file_instance:
            return None
        self._validate_and_handle_file(model_instance, file_instance, add)
        return super().pre_save(model_instance, add)

    def _validate_and_handle_file(self, model_instance, file_instance, add):
        self._validate_file_extension(file_instance)
        if not add:
            self._handle_file_replacement(model_instance)

    def _handle_file_replacement(self, model_instance):
        old_file = self.get_old_file(model_instance)
        new_file = getattr(model_instance, self.name, None)

        if old_file and new_file and old_file != new_file:
            self.storage.delete(old_file.name)
            self.delete_thumbnails(model_instance)

    def _validate_file_extension(self, file_instance):
        ext = os.path.splitext(file_instance.name)[1].lower()
        if self.valid_extensions and ext not in self.valid_extensions:
            raise ValidationError(f"Invalid file extension. Allowed extensions are: {', '.join(self.valid_extensions)}")


class CustomFileInput(forms.fields.FileField):
    default_validators = []
    default_accept = "*/*"

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        if isinstance(widget, FileInput) and "accept" not in widget.attrs:
            attrs.setdefault("accept", self.default_accept)
        return attrs


class CustomImageInput(CustomFileInput):
    default_validators = [
        FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png', 'gif', 'bmp', 'webp', 'tiff'])]
    default_accept = "image/*"


class CustomVideoInput(CustomFileInput):
    default_validators = [FileExtensionValidator(allowed_extensions=['mp4', 'mkv', 'flv', 'avi', 'mov', 'wmv'])]
    default_accept = "video/*"


class DeletableImageField(DeletableMediaField):
    valid_extensions = ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.webp', '.tiff']

    def formfield(self, **kwargs):
        return super().formfield(form_class=CustomImageInput, **kwargs)


class DeletableVideoField(DeletableMediaField):
    valid_extensions = ['.mp4', '.mkv', '.flv', '.avi', '.mov', '.wmv']

    def formfield(self, **kwargs):
        return super().formfield(form_class=CustomVideoInput, **kwargs)


class DeletableFileField(DeletableMediaField):
    def formfield(self, **kwargs):
        return super().formfield(form_class=CustomFileInput, **kwargs)


@receiver(pre_delete)
def delete_file_on_delete(sender, instance, **kwargs):
    for field in instance._meta.fields:
        if isinstance(field, (DeletableImageField, DeletableVideoField, DeletableFileField)):
            field.delete(instance)
            file_field = getattr(instance, field.name)
            if file_field:
                file_field.delete(False)


@receiver(post_save)
def generate_thumbnails_post_save(sender, instance, *args, **kwargs):
    for field in instance._meta.fields:
        if isinstance(field, DeletableImageField) and hasattr(instance, field.name + '_thumbnails'):
            if hasattr(instance, 'local') and instance.local:
                return

            image_field = getattr(instance, field.name)

            # Check if the image field is empty
            if not image_field:
                continue

            sizes = (
                ('s', 220),
                ('m', 640),
                ('l', 960),
            )

            thumbnails_field_name = field.name + '_thumbnails'
            name, ext = image_field.name.split('.')
            storage = image_field.storage

            # Open the image using PIL
            image = Image.open(image_field)
            thumbnails = {}

            for key, value in sizes:
                thumbnail_name = f'{name}_{key}.{ext}'
                thumbnail = image.copy()
                thumbnail.thumbnail((value, value))

                # Create a File object from the in-memory image
                thumb_file = BytesIO()
                thumbnail.save(thumb_file, format=image.format, quality=100)
                thumb_file.seek(0)

                # Save the thumbnail using storage
                storage.save(thumbnail_name, File(thumb_file))

                thumbnails[key] = thumbnail_name

            instance.__class__.objects.filter(pk=instance.pk).update(**{thumbnails_field_name: thumbnails})

