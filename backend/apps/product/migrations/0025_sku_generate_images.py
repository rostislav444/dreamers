# Generated by Django 4.2.3 on 2024-10-22 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0024_alter_skuimages_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='sku',
            name='generate_images',
            field=models.BooleanField(default=True),
        ),
    ]
