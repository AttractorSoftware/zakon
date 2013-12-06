from django import forms


class ReferenceForm(forms.Form):
    source_document_id = forms.HiddenInput()
    source_element = forms.HiddenInput()
    target_document_id = forms.HiddenInput()
    target_element = forms.HiddenInput()