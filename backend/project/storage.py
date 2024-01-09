import mimetypes

import boto3
from botocore.exceptions import NoCredentialsError
from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_str


@deconstructible
class S3Storage(Storage):
    def __init__(self):
        self.bucket_name = 'dreamers'  # ваш бакет
        self.client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                   aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    def _normalize_name(self, name):
        return name

    def _clean_name(self, name):
        return force_str(name.replace('\\', '/'))

    def save(self, name, content, max_length=None):
        cleaned_name = self._clean_name(name)
        content_type, _ = mimetypes.guess_type(cleaned_name)

        try:
            self.client.upload_fileobj(
                content,
                self.bucket_name,
                cleaned_name,
                ExtraArgs={
                    'GrantRead': 'uri="http://acs.amazonaws.com/groups/global/AllUsers"',
                    'ContentType': content_type,
                    'ContentDisposition': 'inline',
                }
            )
        except NoCredentialsError:
            print('Credentials not available')

        return cleaned_name

    def _open(self, name, mode='rb'):
        file = self.client.get_object(Bucket=self.bucket_name, Key=name)
        return file['Body']

    def delete(self, name):
        print('storage delete', name)
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=name)
        except NoCredentialsError:
            print('Credentials not available')

    def exists(self, name):
        try:
            self.client.head_object(Bucket=self.bucket_name, Key=name)
            return True
        except NoCredentialsError:
            print('Credentials not available')
            return False

    def listdir(self, path):
        # Этот метод должен возвращать кортеж (список файлов в директории, список поддиректорий).
        # Реализуйте его с учетом структуры вашего бакета, если это необходимо.
        return [], []

    def path(self, name):
        # Возвращать физический путь к файлу на сервере не требуется при использовании S3.
        # Этот метод может быть просто заглушкой.
        return name

    def size(self, name):
        try:
            file = self.client.head_object(Bucket=self.bucket_name, Key=name)
            return file['ContentLength']
        except NoCredentialsError:
            print('Credentials not available')

    def url(self, name):
        return f'https://{self.bucket_name}.s3.amazonaws.com/{name}'
