# Generated by Django 5.0.6 on 2024-06-30 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0023_alter_orders_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='created',
            field=models.DateField(auto_now=True),
        ),
    ]
