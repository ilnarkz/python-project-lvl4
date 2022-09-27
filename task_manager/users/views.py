from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from task_manager.tasks.models import Task
from task_manager.users.forms import UserForm
from django.utils.translation import gettext_lazy as _


ERROR_URL = reverse_lazy('users:users')
ERROR_MESSAGE = _('You have no permission to delete another user.')


class UserListView(ListView):
    model = get_user_model()
    template_name = 'users/users.html'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = get_user_model()
    form_class = UserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = _('User registered successfully!')


class UserDeleteView(SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = get_user_model()
    success_url = reverse_lazy('users:users')
    template_name = 'users/delete.html'
    success_message = _('User deleted successfully!')

    def test_func(self):
        return self.get_object().id == self.request.user.pk

    def handle_no_permission(self):
        messages.error(
            self.request,
            _('You have no permission to delete another user.')
        )
        return redirect(self.success_url)

    def form_valid(self, form):
        if Task.objects.filter(author_id=self.request.user.pk):
            messages.error(
                self.request,
                _("It is not possible to delete a user because it is in use")
            )
            return redirect(self.success_url)
        return super().form_valid(form)


class UserUpdateView(UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = get_user_model()
    form_class = UserForm
    template_name = 'users/update.html'
    success_message = _('User updated successfully!')

    def test_func(self):
        return self.get_object().id == self.request.user.pk

    def handle_no_permission(self):
        messages.error(
            self.request,
            _('You have no permission to update another user.')
        )
        return redirect(ERROR_URL)
