# Generated by Django 4.2.3 on 2024-09-21 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0019_alter_product3dblendermodel_eye_level_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product3dblendermodel',
            name='eye_level',
            field=models.DecimalField(decimal_places=2, default=1.5, max_digits=3),
        ),
    ]
