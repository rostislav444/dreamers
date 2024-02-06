# Generated by Django 4.0.10 on 2024-02-06 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productclass',
            name='materials_set',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='material.materialsset'),
        ),
        migrations.DeleteModel(
            name='ProductClassMaterialSet',
        ),
    ]