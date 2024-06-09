# Generated by Django 5.0.6 on 2024-05-21 20:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categorie', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('description', models.TextField()),
                ('photo', models.ImageField(upload_to='produit')),
                ('prix', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('marque', models.CharField(blank=True, max_length=1000, null=True)),
                ('modele', models.CharField(blank=True, max_length=1000, null=True)),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categorie.categories')),
            ],
        ),
    ]
