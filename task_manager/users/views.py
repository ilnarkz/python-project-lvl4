from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from task_manager.tasks.models import Task
from task_manager.users.forms import CreateUserForm
from django.utils.translation import gettext_lazy as _


class UserListView(ListView):
    model = get_user_model()
    template_name = 'users/users.html'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = get_user_model()
    form_class = CreateUserForm
    template_name = 'form.html'
    success_url = reverse_lazy('login')
    success_message = _('User registered successfully!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Registration')
        context['button_text'] = _('Sign up')
        return context


class UserDeleteView(UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = get_user_model()
    success_url = reverse_lazy('index')
    template_name = 'delete.html'
    error_url = reverse_lazy('users:users')
    success_message = _('User deleted successfully!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Deleting user')
        context['button_text'] = _('Yes, delete')
        return context

    def test_func(self):
        return self.get_object().id == self.request.user.pk

    def handle_no_permission(self):
        messages.error(
            self.request,
            _('You have no permission to delete another user.')
        )
        return redirect(self.error_url)

    def form_valid(self, form):
        success_message = self.success_message
        if Task.objects.filter(author=self.request.user):
            messages.error(
                self.request,
                _("It is not possible to delete a user because it is in use")
            )
            return redirect(self.error_url)
        self.object.delete()
        messages.success(self.request, success_message)
        return redirect(reverse('users:users'))


class UserUpdateView(UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = get_user_model()
    form_class = CreateUserForm
    template_name = 'form.html'
    error_url = reverse_lazy('users:users')
    success_message = _('User updated successfully!')

    def test_func(self):
        return self.get_object().id == self.request.user.pk

    def handle_no_permission(self):
        messages.error(
            self.request,
            _('You have no permission to update another user.')
        )
        return redirect(self.error_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Updating User')
        context['button_text'] = _('Update')
        return context
