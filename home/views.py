from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import ProjectForm
from .mixins import ProjectAccessMixin
from .models import Project


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'home/index.html'
    model = Project
    ordering = ('pk')
    paginate_by = 20

    def get_queryset(self):
        query = super().get_queryset()
        self.type = self.request.GET.get('type', 'mine')
        if self.type == 'mine':
            return query.filter(members=self.request.user)
        elif self.type == 'all':
            return query.filter(Q(is_private=False) | Q(members=self.request.user)).distinct()
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = self.type
        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'home/project_create.html'
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('home:project_detail', args=(self.object.slug,))


class ProjectDetailView(ProjectAccessMixin, generic.DetailView):
    template_name = 'home/project_detail.html'
    model = Project
    context_object_name = 'project'


class ProjectSettingView(ProjectAccessMixin, generic.UpdateView):
    template_name = 'home/project_setting.html'
    model = Project
    context_object_name = 'project'
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('home:project_detail', args=(self.object.slug,))


class ProjectDeleteView(ProjectAccessMixin, generic.DeleteView):
    template_name = 'home/project_delete.html'
    model = Project
    context_object_name = 'project'
    success_url = reverse_lazy('home:project_list')
