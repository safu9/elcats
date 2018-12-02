from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views import generic


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'home/index.html'


class LoginView(auth_views.LoginView):
    template_name = 'home/login.html'
    redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    template_name = 'home/logout.html'


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'home/password_change.html'
    success_url = reverse_lazy('home:password_change_done')


class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'home/password_change_done.html'


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'home/password_reset.html'
    subject_template_name = 'home/mail/password_reset/subject.txt'
    email_template_name = 'home/mail/password_reset/message.txt'
    success_url = reverse_lazy('home:password_reset_done')


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'home/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'home/password_reset_confirm.html'
    success_url = reverse_lazy('home:password_reset_complete')


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'home/password_reset_complete.html'


class UserView(LoginRequiredMixin, generic.ListView):
    template_name = 'home/user.html'
    paginate_by = 20

    def get_queryset(self):
        return get_user_model().objects.exclude(pk=self.request.user.pk).all()


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'home/user_detail.html'
    model = get_user_model()
    context_object_name = 'object'
    slug_field = 'username'
