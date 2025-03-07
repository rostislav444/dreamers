# Generated by Django 4.2.3 on 2024-10-22 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0005_blendermaterial_aspect_ratio'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecommendedCombinations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('slug', models.SlugField(blank=True, editable=False, max_length=1024, null=True)),
                ('material_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommended_combinations', to='material.materialsset')),
            ],
            options={
                'verbose_name': 'Рекомендованная комбинация',
                'verbose_name_plural': '2. Рекомендованные комбинации',
            },
        ),
        migrations.CreateModel(
            name='RecommendedCombinationsParts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('combination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parts', to='material.recommendedcombinations')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommended_combinations_part', to='material.productpartmaterials')),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommended_combinations', to='material.productpart')),
            ],
        ),
    ]
