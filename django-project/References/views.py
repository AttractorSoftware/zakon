# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from document.models import Document
from References.models import Reference
from References.forms import ReferenceForm
from django.views.generic import View
from update_content import XMLReferenceAdder

SOURCE_DOCUMENT_ID = 'source_document_id'
SOURCE_ELEMENT = 'source_element'
TARGET_DOCUMENT_ID = 'target_document_id'
TARGET_ELEMENT = 'target_element'
HTTP_METHOD_POST = 'POST'
HTTP_REFERER = "HTTP_REFERER"


class AddReferenceView(View):
    def post(self, request):
        ReferenceAdder(request).add_reference()
        return redirect(request.META.get(HTTP_REFERER) + request.POST.get(SOURCE_ELEMENT))


class ReferenceAdder(object):
    def __init__(self, request):
        self.request = request
        self.target_element = self.request.POST.get(TARGET_ELEMENT)
        self.target_document = Document.objects.get(pk=self.request.POST.get(TARGET_DOCUMENT_ID))
        self.source_element = self.request.POST.get(SOURCE_ELEMENT)
        self.source_document = Document.objects.get(pk=self.request.POST.get(SOURCE_DOCUMENT_ID))
        self.form = ReferenceForm(self.request.POST)

    def add_reference(self):
        self.validate_form()
        self.add_reference_and_update_documents()

    def validate_form(self):
        if self.form.is_valid() is False:
            raise self.form.error

    def add_reference_and_update_documents(self):
        self.create_reference()
        self.update_documents()
        self.save_reference()

    def create_reference(self):
        reference = Reference()
        reference.source_document = self.source_document
        reference.source_element = self.source_element
        reference.target_document = self.target_document
        reference.target_element = self.target_element
        self.reference = reference

    def update_documents(self):
        XMLReferenceAdder(self.reference).go()

    def save_reference(self):
        self.reference.save()

