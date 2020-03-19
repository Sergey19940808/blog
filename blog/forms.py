from django.forms import ModelForm
from blog.models import Record


class RecordForm(ModelForm):
    class Meta:
        model = Record
        fields = ['title', 'text']