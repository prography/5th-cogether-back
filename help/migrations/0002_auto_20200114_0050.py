# Generated by Django 2.2.6 on 2020-01-14 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helpcenter',
            name='source',
            field=models.CharField(choices=[('help', 'help'), ('update', 'update'), ('create', 'create')], default='help', max_length=30),
        ),
        migrations.AlterField(
            model_name='helpcenter',
            name='status',
            field=models.CharField(choices=[('waiting', 'waiting'), ('completed', 'completed')], default='waiting', max_length=40),
        ),
    ]
