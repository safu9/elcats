from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin

from .forms import MessageForm
from .models import Channel, ChannelMembership


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'chat/index.html'
    model = Channel
    paginate_by = 20

    def get_queryset(self):
        return Channel.objects.filter(members=self.request.user).all().order_by('-updated_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = [(ch, ch.channelmembership_set.get(user=self.request.user)) for ch in context['object_list']]
        return super().get_context_data(**context)


class ChannelView(UserPassesTestMixin, FormMixin, generic.ListView):
    template_name = 'chat/channel.html'
    paginate_by = 20
    form_class = MessageForm

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(Channel, pk=self.kwargs.get('pk'))
        self.kwargs[self.page_kwarg] = kwargs.get(self.page_kwarg) or request.GET.get(self.page_kwarg) or 'last'

        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        if not self.object.members.filter(pk=self.request.user.pk).exists():
            self.raise_exception = True
            return False
        return True

    def get(self, request, *args, **kwargs):
        membership = self.object.channelmembership_set.get(user=request.user)
        if membership.unread_count > 0:
            membership.unread_count = 0
            membership.save()

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return redirect(self.get_success_url())

    def form_valid(self, form):
        message = form.save(commit=False)
        message.channel = self.object
        message.user = self.request.user
        message.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('chat:channel', args=(self.object.pk,))

    def get_queryset(self):
        return self.object.message_set.all().order_by('posted_at')

    def get_context_data(self, **kwargs):
        context = {
            'channel': self.object
        }
        context.update(kwargs)
        return super().get_context_data(**context)


class NewChannelView(LoginRequiredMixin, FormMixin, generic.DetailView):
    template_name = 'chat/new_channel.html'
    model = get_user_model()
    context_object_name = 'object'
    form_class = MessageForm

    channel = None

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.id == request.user.id:
            return HttpResponseRedirect(reverse('chat:index'))

        channel = Channel.objects.filter_by_members([request.user, self.object]).first()
        if channel:
            return HttpResponseRedirect(reverse('chat:channel', args=(channel.pk,)))

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return redirect(request.build_absolute_uri())

    def form_valid(self, form):
        self.channel = Channel.objects.create()

        ChannelMembership.objects.create(channel=self.channel, user=self.request.user)
        ChannelMembership.objects.create(channel=self.channel, user=self.object)

        message = form.save(commit=False)
        message.channel = self.channel
        message.user = self.request.user
        message.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('chat:channel', args=(self.channel.pk,))
