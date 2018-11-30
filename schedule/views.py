import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import ScheduleForm
from .mixins import WeekCalendarMixin
from .models import Schedule


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'schedule/index.html'
    model = Schedule
    ordering = ('date', 'time_from')
    paginate_by = 20


class WeekView(WeekCalendarMixin, generic.TemplateView):
    template_name = 'schedule/week.html'

    def get_week_schedules(self, first, end):
        data = [[]]
        schedules = Schedule.objects.filter(date__range=(first, end)).order_by('date', 'time_from')
        day = first
        for schedule in schedules:
            while day < schedule.date:
                data.append([])
                day += datetime.timedelta(days=1)
            data[-1].append(schedule)
        while day < end:
            data.append([])
            day += datetime.timedelta(days=1)
        return data

    def get_week_calendar(self):
        data = super().get_week_calendar()
        data['schedules'] = self.get_week_schedules(data['first'], data['last'])
        return data

    def get_context_data(self, **kwargs):
        calendar = self.get_week_calendar()
        calendar['date_list'] = zip(calendar['days'], calendar['schedules'])

        context = super().get_context_data(**kwargs)
        context['calendar'] = calendar
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


class DetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'schedule/detail.html'
    model = Schedule


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
