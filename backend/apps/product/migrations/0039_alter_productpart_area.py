# Generated by Django 4.0.10 on 2023-12-26 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0038_remove_productpartmaterialsgroups_area_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productpart',
            name='area',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
