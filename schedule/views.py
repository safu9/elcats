import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import FormMixin

from .forms import ScheduleForm, ScheduleCommentForm
from .mixins import MonthCalendarMixin, WeekCalendarMixin
from .models import Schedule


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'schedule/index.html'
    model = Schedule
    ordering = ('date', 'time_from')
    paginate_by = 20


def get_date_schedule_dict(dates):
    """ ソート済みのdatetime型リストをキーとしたスケジュールリストの辞書を返す """
    data = { d: [] for d in dates }
    schedules = Schedule.objects.filter(date__range=(dates[0], dates[-1])).order_by('date', 'time_from').iterator()
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


class WeekView(WeekCalendarMixin, generic.TemplateView):
    template_name = 'schedule/week.html'

    def get_week_calendar(self):
        data = super().get_week_calendar()
        data['date_list'] = get_date_schedule_dict(data['days'])
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calendar'] = self.get_week_calendar()
        return context


class MonthView(MonthCalendarMixin, generic.TemplateView):
    template_name = 'schedule/month.html'

    def get_month_calendar(self):
        data = super().get_month_calendar()
        data['date_list'] = get_date_schedule_dict(data['days'])
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calendar'] = self.get_month_calendar()
        return context


class CreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'schedule/create.html'
    form_class = ScheduleForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        form.save_m2m()

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('schedule:detail', args=(self.object.pk,))


class DetailView(LoginRequiredMixin, FormMixin, generic.DetailView):
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
        return reverse('schedule:detail', args=(self.object.pk,))


class UpdateView(UserPassesTestMixin, generic.UpdateView):
    template_name = 'schedule/update.html'
    model = Schedule
    form_class = ScheduleForm

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        self.object = self.get_object()
        if self.object.author != self.request.user:
            self.raise_exception = True
            return False
        return True

    def get_success_url(self):
        return reverse('schedule:detail', args=(self.object.pk,))


class DeleteView(UserPassesTestMixin, generic.DeleteView):
    template_name = 'schedule/delete.html'
    model = Schedule
    success_url = reverse_lazy('schedule:index')

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        self.object = self.get_object()
        if self.object.author != self.request.user:
            self.raise_exception = True
            return False
        return True
