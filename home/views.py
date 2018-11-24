from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'home/index.html'


class LoginView(LoginView):
    template_name = 'home/login.html'
    redirect_authenticated_user = True


class LogoutView(LogoutView):
    template_name = 'home/logout.html'


class UserView(LoginRequiredMixin, ListView):
    template_name = 'home/user.html'
    paginate_by = 20

    def get_queryset(self):
        return get_user_model().objects.exclude(pk=self.request.user.pk).all()


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'home/user_detail.html'
    model = get_user_model()
    slug_field = 'username'
