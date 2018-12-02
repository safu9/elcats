import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import PageForm
from .models import Page


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'wiki/index.html'
    model = Page
    paginate_by = 20


class CreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'wiki/create.html'
    form_class = PageForm

    def get_success_url(self):
        return reverse('wiki:detail', args=(self.object.slug,))


class DetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'wiki/detail.html'
    model = Page


class UpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'wiki/update.html'
    model = Page
    form_class = PageForm

    def get_success_url(self):
        return reverse('wiki:detail', args=(self.object.slug,))


class DeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'wiki/delete.html'
    model = Page
    success_url = reverse_lazy('wiki:index')
