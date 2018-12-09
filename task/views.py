import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max, Min
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin

from home.mixins import ProjectMixin
from .forms import TaskForm, TaskCommentForm
from .models import Task


class IndexView(ProjectMixin, generic.ListView):
    template_name = 'task/index.html'
    model = Task
    ordering = ('-pk')
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


class BoardView(ProjectMixin, generic.ListView):
    template_name = 'task/board.html'
    model = Task
    ordering = ('-pk')

    def get_context_data(self, **kwargs):
        queryset = self.get_queryset()
        task_list = []
        for i, name in Task.STATES:
            task_list.append((name, queryset.filter(state=i)))

        context = super().get_context_data(**kwargs)
        context['task_list'] = task_list
        return context


class GanttView(ProjectMixin, generic.ListView):
    template_name = 'task/gantt.html'
    model = Task
    ordering = ('pk')
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
            chart = dict()
            if task.date_from:
                chart['start'] = (task.date_from - min_date).days
            elif task.date_to:
                chart['start'] = (task.date_to - min_date).days

            if task.date_from and task.date_to:
                chart['length'] = (task.date_to - task.date_from).days
            elif task.date_from or task.date_to:
                chart['length'] = 1

            if task.scheduled_date_from:
                chart['scheduled_start'] = (task.scheduled_date_from - min_date).days
            elif task.scheduled_date_to:
                chart['scheduled_start'] = (task.scheduled_date_to - min_date).days

            if task.scheduled_date_from and task.scheduled_date_to:
                chart['scheduled_length'] = (task.scheduled_date_to - task.scheduled_date_from).days
            elif task.scheduled_date_from or task.scheduled_date_to:
                chart['scheduled_length'] = 1

            yield chart

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

        context['today'] = datetime.date.today()
        context['dates'] = dates
        context['months'] = self.group_dates_by_month(dates, min_date)
        context['charts'] = zip(context['object_list'], self.get_charts(context['object_list'], min_date))
        return context


class CreateView(ProjectMixin, generic.CreateView):
    template_name = 'task/create.html'
    form_class = TaskForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.project
        return kwargs

    def form_valid(self, form):
        q = Task.objects.filter(project=self.project).aggregate(Max('number'))
        if not q['number__max']:
            q['number__max'] = 0

        self.object = form.save(commit=False)
        self.object.project = self.project
        self.object.number = q['number__max'] + 1
        self.object.author = self.request.user
        self.object.save()
        form.save_m2m()

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('task:detail', args=(self.project.slug, self.object.number,))


class DetailView(ProjectMixin, FormMixin, generic.DetailView):
    template_name = 'task/detail.html'
    model = Task
    form_class = TaskCommentForm

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, number=self.kwargs.get('number'))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return redirect(self.get_success_url())

    def form_valid(self, form):
        task = form.save(commit=False)
        task.task = self.object
        task.user = self.request.user
        task.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task:detail', args=(self.project.slug, self.object.number,))


class UpdateView(ProjectMixin, generic.UpdateView):
    template_name = 'task/update.html'
    model = Task
    form_class = TaskForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.project
        return kwargs

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, number=self.kwargs.get('number'))

    def get_success_url(self):
        return reverse('task:detail', args=(self.project.slug, self.object.number,))


class DeleteView(ProjectMixin, generic.DeleteView):
    template_name = 'task/delete.html'
    model = Task

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, number=self.kwargs.get('number'))

    def test_func(self):
        if not super().test_func():
            return False

        self.object = self.get_object()
        if self.object.author != self.request.user:
            self.raise_exception = True
            return False
        return True

    def get_success_url(self):
        return reverse('task:index', args=(self.project.slug,))


class UserTaskView(LoginRequiredMixin, generic.ListView):
    template_name = 'task/user_task.html'
    model = Task
    ordering = ('-pk')
    paginate_by = 20

    def get_queryset(self):
        self.user_object = get_object_or_404(get_user_model(), username=self.kwargs.get('username'))

        query = super().get_queryset().filter(assignees=self.user_object)
        self.state = self.request.GET.get('state', 'undone')
        if self.state == 'undone':
            return query.exclude(state=2)
        elif self.state == 'done':
            return query.filter(state=2)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_object'] = self.user_object
        context['state'] = self.state
        return context
