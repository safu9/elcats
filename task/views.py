import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Max, Min
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import TaskForm
from .models import Task


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'task/index.html'
    model = Task
    paginate_by = 20

    def get_queryset(self):
        query = super().get_queryset()
        self.state = self.request.GET.get('state', 'undone')
        if self.state == 'undone':
            return query.exclude(state=2)
        elif self.state == 'done':
            return query.filter(state=2)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['state'] = self.state
        return context


class BoardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'task/board.html'

    def get_context_data(self, **kwargs):
        task_list = []
        for i, name in Task.STATES:
            task_list.append((name, Task.objects.filter(state=i)))

        context = super().get_context_data(**kwargs)
        context['task_list'] = task_list
        return context


class GanttView(LoginRequiredMixin, generic.ListView):
    template_name = 'task/gantt.html'
    model = Task
    paginate_by = 20

    @staticmethod
    def daterange(date_from, date_to):
        count = ( date_to - date_from ).days + 1
        return [date_from + datetime.timedelta(days=n) for n in range(count)]

    @staticmethod
    def group_dates_by_month(dates, min_date):
        months = [{'date': min_date, 'start': 0, 'length': 0}]
        for date in dates:
            if months[-1]['date'].month == date.month:
                months[-1]['length'] += 1
            else:
                months.append({'date': date, 'length': 1})
        return months

    @staticmethod
    def get_charts(tasks, min_date):
        for task in tasks:
            if task.date_from and task.date_to:
                yield {'start': (task.date_from - min_date).days, 'length': (task.date_to - task.date_from).days}
            elif task.date_from and not task.date_to:
                yield {'start': (task.date_from - min_date).days, 'length': 1}
            elif not task.date_from and task.date_to:
                yield {'start': (task.date_to - min_date).days, 'length': 1}
            else:
                yield None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        q = context['object_list'].aggregate(Min('date_from'), Max('date_to'))
        if not q['date_from__min']:
            q['date_from__min'] = datetime.date.today()
        if not q['date_to__max']:
            q['date_to__max'] = datetime.date.today()

        min_date = q['date_from__min'] - datetime.timedelta(days=7)
        max_date = q['date_to__max'] + datetime.timedelta(days=7)
        dates = self.daterange(min_date, max_date)

        context['dates'] = dates
        context['months'] = self.group_dates_by_month(dates, min_date)
        context['charts'] = zip(context['object_list'], self.get_charts(context['object_list'], min_date))
        return context


class CreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'task/create.html'
    form_class = TaskForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        form.save_m2m()

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('task:detail', args=(self.object.pk,))


class DetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'task/detail.html'
    model = Task


class UpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'task/update.html'
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse('task:detail', args=(self.object.pk,))


class DeleteView(UserPassesTestMixin, generic.DeleteView):
    template_name = 'task/delete.html'
    model = Task
    success_url = reverse_lazy('task:index')

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        self.object = self.get_object()
        if self.object.author != self.request.user:
            self.raise_exception = True
            return False
        return True
