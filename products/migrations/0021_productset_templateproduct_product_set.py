# Generated by Django 4.2.5 on 2023-09-29 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0001_initial'),
        ('products', '0020_remove_templateproduct_product_set_delete_productset'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productset_name', models.CharField(max_length=255)),
                ('total_productset_price', models.FloatField(max_length=255)),
                ('object', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='objects.object')),
            ],
        ),
        migrations.AddField(
            model_name='templateproduct',
            name='product_set',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.productset'),
        ),
    ]
