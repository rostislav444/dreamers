# Generated by Django 4.0.10 on 2023-11-21 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attribute', '0018_alter_attribute_options'),
        ('product', '0022_alter_productclassoption_value_color_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productclassoptiongroup',
            name='attribute_sub_group',
            field=models.ManyToManyField(blank=True, to='attribute.attributesubgroup'),
        ),
    ]
