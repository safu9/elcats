import datetime

from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin

from home.mixins import ProjectMixin
from .forms import ScheduleForm, ScheduleCommentForm
from .mixins import MonthCalendarMixin, WeekCalendarMixin
from .models import Schedule


class IndexView(ProjectMixin, generic.ListView):
    template_name = 'schedule/index.html'
    model = Schedule
    ordering = ('date', 'time_from')
    paginate_by = 20


class BaseCalendarView(ProjectMixin, generic.ListView):
    model = Schedule
    ordering = ('date', 'time_from')

    def get_date_schedule_dict(self, dates):
        """ ソート済みのdatetime型リストをキーとしたリストの辞書を返す """
        data = { d: [] for d in dates }
        schedules = self.get_queryset().filter(date__range=(dates[0], dates[-1])).iterator()
        schedule = next(schedules, None)

        for day, list in data.items():
            if not schedule:
                break
            if day < schedule.date:
                continue
            while schedule and day == schedule.date:
                list.append(schedule)
                schedule = next(schedules, None)
        return data


class WeekView(WeekCalendarMixin, BaseCalendarView):
    template_name = 'schedule/week.html'

    def get_week_calendar(self):
        data = super().get_week_calendar()
        data['date_list'] = self.get_date_schedule_dict(data['days'])
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calendar'] = self.get_week_calendar()
        return context


class MonthView(MonthCalendarMixin, BaseCalendarView):
    template_name = 'schedule/month.html'

    def get_month_calendar(self):
        data = super().get_month_calendar()
        data['date_list'] = self.get_date_schedule_dict(data['days'])
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calendar'] = self.get_month_calendar()
        return context


class CreateView(ProjectMixin, generic.CreateView):
    template_name = 'schedule/create.html'
    form_class = ScheduleForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.project = self.project
        self.object.author = self.request.user
        self.object.save()
        form.save_m2m()

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('schedule:detail', args=(self.project.slug, self.object.pk,))


class DetailView(ProjectMixin, FormMixin, generic.DetailView):
    template_name = 'schedule/detail.html'
    model = Schedule
    form_class = ScheduleCommentForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return redirect(self.get_success_url())

    def form_valid(self, form):
        task = form.save(commit=False)
        task.schedule = self.object
        task.user = self.request.user
        task.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('schedule:detail', args=(self.project.slug, self.object.pk,))


class UpdateView(ProjectMixin, generic.UpdateView):
    template_name = 'schedule/update.html'
    model = Schedule
    form_class = ScheduleForm

    def test_func(self):
        if not super().test_func():
            return False

        self.object = self.get_object()
        if self.object.author != self.request.user:
            self.raise_exception = True
            return False
        return True

    def get_success_url(self):
        return reverse('schedule:detail', args=(self.project.slug, self.object.pk,))


class DeleteView(ProjectMixin, generic.DeleteView):
    template_name = 'schedule/delete.html'
    model = Schedule

    def test_func(self):
        if not super().test_func():
            return False

        self.object = self.get_object()
        if self.object.author != self.request.user:
            self.raise_exception = True
            return False
        return True

    def get_success_url(self):
        return reverse('schedule:index', args=(self.project.slug,))
