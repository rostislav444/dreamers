# Generated by Django 4.0.10 on 2023-12-20 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_productpartcolor'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductPartMaterial',
            new_name='ProductPart',
        ),
    ]