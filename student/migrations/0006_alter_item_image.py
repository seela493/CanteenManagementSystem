# Generated by Django 5.1 on 2024-08-31 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
