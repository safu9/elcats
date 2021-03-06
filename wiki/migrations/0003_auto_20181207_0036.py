# Generated by Django 2.1 on 2018-12-06 15:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
        ('wiki', '0002_page_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.SlugField(validators=[django.core.validators.RegexValidator(inverse_match=True, message='このスラッグは利用できません。', regex='^create$')], verbose_name='スラッグ'),
        ),
        migrations.AlterUniqueTogether(
            name='page',
            unique_together={('project', 'slug')},
        ),
    ]
