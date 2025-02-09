# Generated by Django 5.0.6 on 2024-06-14 09:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_alter_orders_dish'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, max_length=250, null=True, upload_to='images/')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.dish')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to='base.restaurants')),
            ],
        ),
    ]
