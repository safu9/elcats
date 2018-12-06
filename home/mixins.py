from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Project


class ProjectAccessMixin(UserPassesTestMixin):

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        self.object = self.get_object()
        if self.object.is_private and self.request.user not in self.object.members.all:
            self.raise_exception = True
            return False
        return True


class ProjectMixin(UserPassesTestMixin):

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        self.project = self.get_project()
        if self.project.is_private and self.request.user not in self.project.members.all:
            self.raise_exception = True
            return False
        return True

    def get_project(self):
        if getattr(self, 'project', None) and isinstance(self.project, Project):
            return self.project

        self.project = Project.objects.get(slug=self.kwargs['project'])
        return self.project

    def get_queryset(self):
        return super().get_queryset().filter(project=self.project)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        return context
