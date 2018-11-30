from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView


from .forms import ScheduleForm
from .models import Schedule


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'schedule/index.html'
    model = Schedule
    paginate_by = 20


class CreateView(LoginRequiredMixin, CreateView):
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


class DetailView(LoginRequiredMixin, DetailView):
    template_name = 'schedule/detail.html'
    model = Schedule


class UpdateView(UserPassesTestMixin, UpdateView):
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


class DeleteView(UserPassesTestMixin, DeleteView):
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
