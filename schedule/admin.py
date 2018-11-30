from django.contrib import admin

from .models import Schedule, ScheduleOccurence


admin.site.register(Schedule)
admin.site.register(ScheduleOccurence)
