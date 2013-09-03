from django import forms


class UploadForm(forms.Form):
    doc_file = forms.FileField()


class WrapTextForm(forms.Form):
    document_id = forms.HiddenInput()
    article_id = forms.HiddenInput()
    start_position = forms.HiddenInput()
    length = forms.HiddenInput()
    reference_url=forms.TextInput()