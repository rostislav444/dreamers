# Generated by Django 4.0 on 2022-08-03 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attribute', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attributegroup',
            name='custom',
            field=models.BooleanField(default=False),
        ),
    ]
