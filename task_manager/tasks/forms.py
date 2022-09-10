from django.forms import ModelForm, ModelMultipleChoiceField, SelectMultiple

from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class CreateTaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'labels', 'performer']
