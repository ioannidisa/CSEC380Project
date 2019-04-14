from django import forms


class VideoForm(forms.Form):
    name = forms.CharField(label='Title')
    desc = forms.CharField(label='Description')
    file = forms.FileField(label='Select a file')


class DeleteForm(forms.Form):
    id = forms.IntegerField()
