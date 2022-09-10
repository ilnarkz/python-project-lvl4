from django.forms import ModelForm
from task_manager.tasks.models import Task


class CreateTaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'labels', 'performer']
