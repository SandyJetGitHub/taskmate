from django.forms import ModelForm
from todolist_app.models import TaskList

class TaskForms(ModelForm):
    class Meta:
        model = TaskList
        fields = ['task', 'done']
