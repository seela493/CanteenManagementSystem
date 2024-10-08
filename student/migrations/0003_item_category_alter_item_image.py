# Generated by Django 5.1 on 2024-08-30 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_order_is_ordered_alter_item_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('veg', 'Vegetarian'), ('non-veg', 'Non-Vegetarian'), ('drink', 'Drink')], default='veg', max_length=10),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/imgages'),
        ),
    ]
