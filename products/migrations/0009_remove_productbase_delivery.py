# Generated by Django 4.1.7 on 2023-08-23 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_productbase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productbase',
            name='delivery',
        ),
    ]