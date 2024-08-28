# Generated by Django 4.2.3 on 2024-08-10 10:26

import apps.abstract.fields.fields_image
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('interior', '0001_initial'),
        ('product', '0015_productclass_interior'),
    ]

    operations = [
        migrations.CreateModel(
            name='CameraLocationsInteriorLayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CameraLocationsInteriorLayerMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RenameModel(
            old_name='CameraLocations',
            new_name='Camera',
        ),
        migrations.CreateModel(
            name='CameraLocationsInteriorLayerMaterialImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', apps.abstract.fields.fields_image.DeletableImageField(upload_to='')),
                ('image_thumbnails', models.JSONField(blank=True, default=dict, null=True)),
                ('scene_material', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='product.cameralocationsinteriorlayermaterial')),
            ],
        ),
        migrations.CreateModel(
            name='CameraLocationsInteriorLayerMaterialGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('layer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_groups', to='product.cameralocationsinteriorlayer')),
                ('material_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cameras', to='interior.interiorlayermaterialgroup')),
            ],
        ),
        migrations.AddField(
            model_name='cameralocationsinteriorlayermaterial',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='product.cameralocationsinteriorlayermaterialgroup'),
        ),
        migrations.AddField(
            model_name='cameralocationsinteriorlayermaterial',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_scene', to='interior.interiormaterial'),
        ),
        migrations.AddField(
            model_name='cameralocationsinteriorlayer',
            name='camera',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interior_layers', to='product.camera'),
        ),
        migrations.AddField(
            model_name='cameralocationsinteriorlayer',
            name='interior_layer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cameras', to='interior.interiorlayer'),
        ),
    ]