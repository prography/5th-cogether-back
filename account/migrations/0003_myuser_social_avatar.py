# Generated by Django 2.2.6 on 2019-12-05 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20191205_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='social_avatar',
            field=models.URLField(blank=True),
        ),
    ]
