# Generated by Django 2.2.6 on 2020-01-13 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20200108_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devevent',
            name='status',
            field=models.CharField(choices=[('development', '개발 행사'), ('not_development', '비개발 행사'), ('unclassified_events', '미분류 행사')], default='unclassified_events', max_length=30),
        ),
    ]
