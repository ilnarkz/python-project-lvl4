from django.forms import ModelForm
from task_manager.statuses.models import Status


class CreateStatusForm(ModelForm):

    class Meta:
        model = Status
        fields = ['name']
