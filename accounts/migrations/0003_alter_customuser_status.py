# Generated by Django 4.1.7 on 2023-08-17 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_name_alter_customuser_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
