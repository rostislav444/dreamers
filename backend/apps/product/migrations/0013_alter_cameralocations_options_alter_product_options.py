# Generated by Django 4.2.3 on 2024-07-21 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cameralocations',
            options={'ordering': ['-rad_z'], 'verbose_name': 'Камера', 'verbose_name_plural': 'Камеры'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['product_class', 'width', 'height', 'depth'], 'verbose_name': 'Вариант', 'verbose_name_plural': '2. Варианты'},
        ),
    ]
