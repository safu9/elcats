from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView


from .forms import ScheduleForm
from .models import Schedule


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'schedule/index.html'
    model = Schedule
    paginate_by = 20


class CreateView(LoginRequiredMixin, CreateView):
    template_name = 'schedule/create.html'
    form_class = ScheduleForm
    success_url = reverse_lazy('schedule:index')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        form.save_m2m()

        return redirect(self.get_success_url())


class DetailView(LoginRequiredMixin, DetailView):
    template_name = 'schedule/detail.html'
    model = Schedule
