# Generated by Django 4.0.10 on 2023-12-28 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0043_alter_skumaterials_material'),
    ]

    operations = [
        migrations.AddField(
            model_name='productpartmaterials',
            name='show_in_catalogue',
            field=models.BooleanField(default=True),
        ),
    ]