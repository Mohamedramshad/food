# Generated by Django 5.1.1 on 2024-11-08 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_alter_address_landmark_alter_address_phone'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'ordering': ['-id'], 'verbose_name': 'address', 'verbose_name_plural': 'addresses'},
        ),
        migrations.AlterModelTable(
            name='address',
            table='Customer_address',
        ),
    ]
