# Generated by Django 4.2.3 on 2024-08-10 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0001_initial'),
        ('product', '0014_productpartscenematerialimage_image_thumbnails'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='sku',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='product.sku'),
        ),
        migrations.CreateModel(
            name='OrderItemMaterials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='order.orderitem')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='material.productpartmaterials')),
            ],
        ),
    ]
