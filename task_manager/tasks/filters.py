import django_filters
from django.forms import CheckboxInput
from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from django.utils.translation import gettext_lazy as _


class TaskFilter(django_filters.FilterSet):
    labels = django_filters.ModelChoiceFilter(
        label=_('Label'),
        queryset=Label.objects.all()
    )
    self_tasks = django_filters.BooleanFilter(
        label=_('Only self tasks'),
        widget=CheckboxInput, method='get_self_tasks'
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'self_tasks']

    def get_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
