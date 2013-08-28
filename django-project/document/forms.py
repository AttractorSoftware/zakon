from django import forms


class UploadForm(forms.Form):
    doc_file = forms.FileField()


class WrapTextForm(forms.Form):
    document_id = forms.HiddenInput()
    article_id = forms.HiddenInput()
    content = forms.HiddenInput()