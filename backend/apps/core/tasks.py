from botocore.exceptions import NoCredentialsError
from celery import shared_task

from project import settings


@shared_task
def async_s3_file_delete(bucket_name, name):
    storage = settings.FILE_STORAGE()
    client = storage.client

    try:
        client.delete_object(Bucket=bucket_name, Key=name)
    except NoCredentialsError:
        print('Credentials not available')
