# Generated by Django 4.0.8 on 2022-12-06 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_productoptionpricemultiplier_product'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productclassoption',
            options={'ordering': ('value_attribute', 'value_text', 'value_integer', 'value_boolean', 'value_float', 'value_color_hex', 'value_min', 'value_max', 'value_image_name')},
        ),
    ]
