# Generated by Django 4.2.3 on 2025-02-19 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0015_alter_productpartmaterials_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material',
            name='type',
        ),
    ]
