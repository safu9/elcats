from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import TaskForm
from .models import Task


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'task/index.html'
    model = Task
    paginate_by = 20


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
