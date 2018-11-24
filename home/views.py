from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'home/index.html'


class LoginView(LoginView):
    template_name = 'home/login.html'
    redirect_authenticated_user = True


class LogoutView(LogoutView):
    template_name = 'home/logout.html'
