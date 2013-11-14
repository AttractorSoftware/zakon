# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from References.dom_modifier import update_xml_of_linked_document, update_xml_of_reference_document
from document.models import Document
from References.models import Reference
from References.forms import WrapTextForm


def wrap_text_in_tag(request):
    if request.method == 'POST':
        form = WrapTextForm(request.POST)
        if form.is_valid():
            ref = Reference()
            ref.reference_document = Document.objects.get(pk=request.POST.get('reference_document_id'))
            ref.reference_element = request.POST.get('reference_element')
            ref.linked_document = Document.objects.get(pk=request.POST.get('linked_document_id'))
            ref.linked_element = request.POST.get('linked_element')

            reference_document = ref.reference_document
            linked_document = ref.linked_document

            ref.save()
            reference_document.content = update_xml_of_reference_document(reference_document.content,
                                                                          ref.reference_element, ref.linked_document.id,
                                                                          ref.linked_element)
            reference_document.save()
            linked_document.content = update_xml_of_linked_document(linked_document.content, ref.linked_element,
                                                                    ref.reference_document.id,
                                                                    ref.reference_element)
            linked_document.save()
    return redirect(request.META.get("HTTP_REFERER") + ref.reference_element)
