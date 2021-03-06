# Generated by Django 2.1 on 2018-12-05 07:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='名前')),
                ('slug', models.SlugField(verbose_name='スラッグ')),
                ('description', models.TextField(blank=True, max_length=50, verbose_name='説明')),
                ('is_private', models.BooleanField(default=False, verbose_name='非公開')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='メンバー')),
            ],
            options={
                'verbose_name': 'プロジェクト',
                'verbose_name_plural': 'プロジェクト',
            },
        ),
    ]
