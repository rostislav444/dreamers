# Generated by Django 4.2.3 on 2024-12-01 16:39

import apps.abstract.fields.fields_image
from django.db import migrations
import project.storage


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0011_materialsset_copy_from'),
    ]

    operations = [
        migrations.AddField(
            model_name='blendermaterial',
            name='preview',
            field=apps.abstract.fields.fields_image.DeletableImageField(blank=True, null=True, storage=project.storage.S3Storage, upload_to='', verbose_name='Preview'),
        ),
    ]
