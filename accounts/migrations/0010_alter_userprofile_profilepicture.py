# Generated by Django 5.0.6 on 2024-06-29 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_userprofile_profilepicture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profilePicture',
            field=models.ImageField(blank=True, default='/images/default.avif', null=True, upload_to='accouts/'),
        ),
    ]
