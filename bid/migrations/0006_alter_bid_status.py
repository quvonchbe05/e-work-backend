# Generated by Django 4.1.7 on 2023-09-15 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bid', '0005_alter_bidtowarehouse_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='status',
            field=models.CharField(default='yuborilgan', max_length=244),
        ),
    ]