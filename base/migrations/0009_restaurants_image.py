# Generated by Django 5.0.6 on 2024-05-31 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_restaurants_options_alter_dish_dishimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurants',
            name='image',
            field=models.FileField(blank=True, null='True', upload_to='restaurant_images'),
            preserve_default='True',
        ),
    ]
