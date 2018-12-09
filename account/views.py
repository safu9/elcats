from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import ProfileForm


class LoginView(auth_views.LoginView):
    template_name = 'account/login.html'
    redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    template_name = 'account/logout.html'


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'account/password_change.html'
    success_url = reverse_lazy('account:password_change_done')


class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'account/password_change_done.html'


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset.html'
    subject_template_name = 'account/mail/password_reset/subject.txt'
    email_template_name = 'account/mail/password_reset/message.txt'
    success_url = reverse_lazy('account:password_reset_done')


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class UserView(LoginRequiredMixin, generic.ListView):
    template_name = 'account/user.html'
    model = get_user_model()
    ordering = ('pk')
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'account/user_detail.html'
    model = get_user_model()
    context_object_name = 'object'
    slug_field = 'username'


class ProfileView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'account/profile.html'
    model = get_user_model()
    form_class = ProfileForm
    context_object_name = 'object'

    def get_object(self, queryset=None):
        return self.get_queryset().get(pk=self.request.user.pk)

    def get_success_url(self):
        return reverse('account:user_detail', args=(self.object.username,))
