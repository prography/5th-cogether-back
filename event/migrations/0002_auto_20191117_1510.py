# Generated by Django 2.2.3 on 2019-11-17 15:10

import cogether.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='image',
        ),
        migrations.AddField(
            model_name='event',
            name='photo',
            field=models.ImageField(blank=True, upload_to=cogether.utils.uuid_name_upload_to),
        ),
    ]
