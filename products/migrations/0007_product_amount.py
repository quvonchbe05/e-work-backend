# Generated by Django 4.1.7 on 2023-08-22 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_templateproduct_remove_product_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
