# Generated by Django 2.1 on 2018-11-30 02:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import recurrence.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='名前')),
                ('description', models.TextField(blank=True, verbose_name='説明')),
                ('place', models.CharField(blank=True, max_length=50, verbose_name='場所')),
                ('date', models.DateField(verbose_name='日付')),
                ('time_from', models.TimeField(blank=True, null=True, verbose_name='開始時間')),
                ('time_to', models.TimeField(blank=True, null=True, verbose_name='終了時間')),
                ('recurrence', recurrence.fields.RecurrenceField(blank=True, verbose_name='繰り返し条件')),
                ('recur_until', models.DateField(blank=True, null=True, verbose_name='繰り返し終了日')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authored_schedules', to=settings.AUTH_USER_MODEL, verbose_name='作成者')),
                ('participants', models.ManyToManyField(blank=True, related_name='participated_schedules', to=settings.AUTH_USER_MODEL, verbose_name='参加者')),
            ],
            options={
                'verbose_name': '予定',
                'verbose_name_plural': '予定',
            },
        ),
        migrations.CreateModel(
            name='ScheduleOccurence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='日付')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.Schedule', verbose_name='予定')),
            ],
            options={
                'verbose_name': '実予定',
                'verbose_name_plural': '実予定',
            },
        ),
    ]
