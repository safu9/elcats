# Generated by Django 2.1 on 2018-12-07 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='スラッグ'),
        ),
    ]
