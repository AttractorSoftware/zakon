from django import forms


class WrapTextForm(forms.Form):
    reference_document_id = forms.HiddenInput()
    reference_element = forms.HiddenInput()
    linked_document_id = forms.HiddenInput()
    linked_element = forms.HiddenInput()