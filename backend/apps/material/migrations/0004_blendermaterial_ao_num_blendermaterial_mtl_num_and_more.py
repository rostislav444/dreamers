# Generated by Django 4.2.3 on 2024-09-21 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0003_alter_color_options_productpartmaterials_preferred'),
    ]

    operations = [
        migrations.AddField(
            model_name='blendermaterial',
            name='ao_num',
            field=models.DecimalField(blank=True, decimal_places=2, default=1.0, max_digits=5, verbose_name='AO Value'),
        ),
        migrations.AddField(
            model_name='blendermaterial',
            name='mtl_num',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5, verbose_name='Metalness Value'),
        ),
        migrations.AddField(
            model_name='blendermaterial',
            name='refl_num',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.5, max_digits=5, verbose_name='Reflection Value'),
        ),
        migrations.AddField(
            model_name='blendermaterial',
            name='rgh_num',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.5, max_digits=5, verbose_name='Roughness Value'),
        ),
        migrations.AddField(
            model_name='blendermaterial',
            name='scale',
            field=models.DecimalField(blank=True, decimal_places=2, default=1, max_digits=5, verbose_name='Scale'),
        ),
    ]
