from django import forms


class UploadForm(forms.Form):
    doc_file = forms.FileField()
