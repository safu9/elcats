import datetime

from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from home.mixins import ProjectMixin
from .forms import PageForm
from .models import Page


class IndexView(ProjectMixin, generic.ListView):
    template_name = 'wiki/index.html'
    model = Page
    ordering = ('pk')
    paginate_by = 20


class CreateView(ProjectMixin, generic.CreateView):
    template_name = 'wiki/create.html'
    form_class = PageForm

    def get_initial(self):
        return {'project': self.project.id}

    def get_success_url(self):
        return reverse('wiki:detail', args=(self.project.slug, self.object.slug))


class DetailView(ProjectMixin, generic.DetailView):
    template_name = 'wiki/detail.html'
    model = Page


class UpdateView(ProjectMixin, generic.UpdateView):
    template_name = 'wiki/update.html'
    model = Page
    form_class = PageForm

    def get_success_url(self):
        return reverse('wiki:detail', args=(self.project.slug, self.object.slug))


class DeleteView(ProjectMixin, generic.DeleteView):
    template_name = 'wiki/delete.html'
    model = Page

    def get_success_url(self):
        return reverse('wiki:index', args=(self.project.slug,))
