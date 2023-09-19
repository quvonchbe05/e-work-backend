# Generated by Django 4.1.7 on 2023-09-19 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0001_initial'),
        ('warehouses', '0003_alter_warehouse_worker'),
        ('bid', '0007_bidtowarehouse_bid_objectproducts'),
    ]

    operations = [
        migrations.AddField(
            model_name='objectproducts',
            name='object',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='object_products', to='objects.object'),
        ),
        migrations.AddField(
            model_name='objectproducts',
            name='warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='object_products', to='warehouses.warehouse'),
        ),
    ]
