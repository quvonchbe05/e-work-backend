# Generated by Django 4.1.7 on 2023-08-22 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_delivery_alter_product_warehouse'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
