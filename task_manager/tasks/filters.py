import django_filters
from django.forms import CheckboxInput
from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    labels = django_filters.ModelChoiceFilter(queryset=Label.objects.all())
    self_tasks = django_filters.BooleanFilter(
        label='only self tasks', widget=CheckboxInput, method='get_self_tasks')

    class Meta:
        model = Task
        fields = ['status', 'performer', 'labels', 'self_tasks']

    def get_self_tasks(self, queryset, name, value):
        if value:
            author = getattr(self.request, 'user', None)
            return queryset.filter(author=author)
        return queryset
