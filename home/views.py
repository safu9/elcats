from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import ProjectForm
from .mixins import ProjectAccessMixin
from .models import Project


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'home/index.html'


class ProjectListView(LoginRequiredMixin, generic.ListView):
    template_name = 'home/project_list.html'
    model = Project
    paginate_by = 20


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'home/project_create.html'
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('home:project_detail', args=(self.object.slug,))


class ProjectDetailView(ProjectAccessMixin, generic.DetailView):
    template_name = 'home/project_detail.html'
    model = Project


class ProjectUpdateView(ProjectAccessMixin, generic.UpdateView):
    template_name = 'home/project_update.html'
    model = Project
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('home:project_detail', args=(self.object.slug,))


class ProjectDeleteView(ProjectAccessMixin, generic.DeleteView):
    template_name = 'home/project_delete.html'
    model = Project
    success_url = reverse_lazy('home:project_list')
