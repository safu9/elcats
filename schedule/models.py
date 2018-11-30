from django.conf import settings
from django.db import models

from recurrence.fields import RecurrenceField


class Schedule(models.Model):

    name = models.CharField('名前', max_length=50)
    description = models.TextField('説明', blank=True)
    place = models.CharField('場所', max_length=50, blank=True)
    date = models.DateField('日付')
    time_from = models.TimeField('開始時間', blank=True, null=True)
    time_to = models.TimeField('終了時間', blank=True, null=True)
    recurrence = RecurrenceField(include_dtstart=False, blank=True, verbose_name='繰り返し条件')
    recur_until = models.DateField('繰り返し終了日', blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authored_schedules', verbose_name='作成者')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='participated_schedules', verbose_name='参加者')

    def get_occurence_dates(self, start, end):
        if start < self.date:
            start = self.date
        if self.recur_until < end:
            end = self.recur_until
        if end < start:
            return []

        return self.recurrence.between(start, end, dtstart=start, inc=True)

    class Meta:
        verbose_name = '予定'
        verbose_name_plural = '予定'


class ScheduleOccurence(models.Model):

    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, verbose_name='予定')
    date = models.DateField('日付')

    class Meta:
        verbose_name = '実予定'
        verbose_name_plural = '実予定'
