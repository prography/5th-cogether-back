# Generated by Django 2.2.6 on 2019-11-04 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('host', models.CharField(blank=True, default='', max_length=100)),
                ('content', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_at', models.DateTimeField(blank=True)),
                ('end_at', models.DateTimeField(blank=True)),
                ('external_link', models.URLField(blank=True, default='')),
                ('location', models.CharField(blank=True, default='', max_length=200)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.Category')),
            ],
            options={
                'ordering': ['start_at'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EventTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.Event')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.Tag')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='tag',
            field=models.ManyToManyField(through='event.EventTag', to='event.Tag'),
        ),
    ]
