from django import forms


class VideoForm(forms.Form):
    name = forms.CharField(label='Title')
    desc = forms.CharField(label='Description')
    file = forms.FileField(label='Select a file', required=False)
    url = forms.CharField(label='URL', required=False)


class DeleteForm(forms.Form):
    id = forms.IntegerField()
