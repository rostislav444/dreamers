# Generated by Django 4.2.3 on 2025-01-29 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0034_productcustomizedpartmaterialgroup_group_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcustomizedpartmaterialgroup',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_groups', to='product.productcustomizedpart'),
        ),
    ]
