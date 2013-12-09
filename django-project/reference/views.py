# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.views.generic import View

from reference.adder import ReferenceAdder, SOURCE_ELEMENT

HTTP_METHOD_POST = 'POST'
HTTP_REFERER = "HTTP_REFERER"


class AddReferenceView(View):
    def post(self, request):
        ReferenceAdder(request).add_reference()
        return redirect(request.META.get(HTTP_REFERER) + request.POST.get(SOURCE_ELEMENT))


