# Generated by Django 4.0 on 2022-08-02 18:01

import apps.attribute.abstract.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('attribute', '0001_initial'),
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=255, null=True, verbose_name='Code')),
                ('price', models.PositiveIntegerField(blank=True, null=True, verbose_name='Price')),
                ('stock', models.PositiveIntegerField(blank=True, null=True, verbose_name='Stock')),
            ],
        ),
        migrations.CreateModel(
            name='ProductClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('slug', models.SlugField(blank=True, editable=False, max_length=1024, null=True)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductClassOptionGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=1024, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('type', apps.attribute.abstract.fields.OptionGroupField(choices=[('attribute', 'Attribute'), ('text', 'Text'), ('integer', 'Integer'), ('boolean', 'Boolean'), ('float', 'Float'), ('color', 'Color'), ('range', 'Range'), ('image', 'Image')], default='attribute', max_length=24, verbose_name='Type')),
                ('save_all_options', models.BooleanField(default=True)),
                ('attribute_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_class_option_group', to='attribute.attributegroup')),
                ('product_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productclass')),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='attribute.attributegroupunit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sku',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=255, null=True)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('slug', models.SlugField(blank=True, editable=False, max_length=1024, null=True)),
                ('value', models.CharField(max_length=255)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product/')),
                ('image_thumb', models.ImageField(blank=True, null=True, upload_to='product/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductClassProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('slug', models.SlugField(blank=True, editable=False, max_length=1024, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='product.productclass')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='category.properties')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductClassOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_text', models.CharField(blank=True, max_length=500, null=True, verbose_name='Text')),
                ('value_integer', models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Integer')),
                ('value_boolean', models.BooleanField(blank=True, db_index=True, null=True, verbose_name='Boolean')),
                ('value_float', models.FloatField(blank=True, db_index=True, null=True, verbose_name='Float')),
                ('value_color_name', models.CharField(blank=True, max_length=500, null=True, verbose_name='Color')),
                ('value_color_hex', models.CharField(blank=True, max_length=7, null=True, verbose_name='Color HEX')),
                ('value_color_image', apps.attribute.abstract.fields.AttributeImageField(blank=True, null=True, storage=apps.attribute.abstract.fields.OverwriteStorage, upload_to='', verbose_name='Color IMAGE')),
                ('value_image_name', models.CharField(blank=True, max_length=500, null=True, verbose_name='Name')),
                ('value_image_image', apps.attribute.abstract.fields.AttributeImageField(blank=True, max_length=500, null=True, storage=apps.attribute.abstract.fields.OverwriteStorage, upload_to='', verbose_name='Image')),
                ('value_min', models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Min')),
                ('value_max', models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Max')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=1024, null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productclassoptiongroup')),
                ('value_attribute', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='attribute.attribute')),
            ],
            options={
                'ordering': ('value_attribute', 'value_text', 'value_integer', 'value_boolean', 'value_float', 'value_color_name', 'value_min', 'value_max', 'value_image_name'),
                'unique_together': {('group', 'value_color_name', 'value_color_hex', 'value_color_image'), ('group', 'value_boolean'), ('group', 'value_attribute'), ('group', 'value_integer'), ('group', 'value_float'), ('group', 'value_min', 'value_max'), ('group', 'value_text')},
            },
        ),
        migrations.CreateModel(
            name='ProductAttributeOptionImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('product_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productclassoption')),
            ],
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='attribute.attribute')),
                ('attribute_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='attribute.attributegroup')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='product.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='product_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productclass'),
        ),
        migrations.CreateModel(
            name='SkuOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.productclassoption')),
                ('option_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.productclassoptiongroup')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='product.sku')),
            ],
            options={
                'ordering': ('sku', 'option'),
                'unique_together': {('sku', 'option')},
            },
        ),
    ]
