# Generated by Django 2.2.6 on 2020-01-18 17:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('help', '0002_auto_20200114_0050'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contents', models.TextField()),
                ('title', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('help', '1:1 요청'), ('update', '수정 요청'), ('create', '게시 요청')], default='help', max_length=30)),
                ('status', models.CharField(choices=[('waiting', '답변 대기중'), ('completed', '답변 완료')], default='waiting', max_length=40)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('answer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='help.Answer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='helpcenter',
            name='user',
        ),
        migrations.DeleteModel(
            name='HelpInfo',
        ),
        migrations.DeleteModel(
            name='HelpCenter',
        ),
    ]
