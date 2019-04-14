from django import forms
from django.core.validators import FileExtensionValidator


class VideoForm(forms.Form):
    name = forms.CharField(label='Title')
    desc = forms.CharField(label='Description')
    file = forms.FileField(label='Select a file', validators=[FileExtensionValidator(allowed_extensions=['.mp4'])])


class DeleteForm(forms.Form):
    id = forms.IntegerField()
