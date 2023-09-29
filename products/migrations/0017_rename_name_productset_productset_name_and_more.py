# Generated by Django 4.2.5 on 2023-09-29 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_alter_productset_total_price_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productset',
            old_name='name',
            new_name='productset_name',
        ),
        migrations.RenameField(
            model_name='productset',
            old_name='total_price',
            new_name='total_productset_price',
        ),
        migrations.AlterField(
            model_name='templateproduct',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='templateproduct',
            name='total_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
