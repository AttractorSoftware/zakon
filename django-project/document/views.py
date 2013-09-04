from itertools import chain

from lxml import etree
from django.core.files.uploadedfile import UploadedFile
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from lxml.etree import tostring
from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.plaintext.writer import PlaintextWriter
from document.add_reference import AddReference

from forms import *
from document.xslt_converter.converter import XsltTransformer
from forms import UploadForm
from models import Document
from LawParser.DOMParser import Parser


def get_file_type(url):
    file_types = [".txt", ".rtf"]
    name_file = str(url)
    for i in file_types:
        if name_file.endswith(i):
            return i


def upload_file(request):
    error_message = ''
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            name_of_upload_file = UploadedFile(request.FILES['doc_file'])
            uploaded_date = timezone.now()
            uploaded_file = request.FILES['doc_file']
            parser = Parser()
            if get_file_type(name_of_upload_file) == ".rtf":
                temp = Rtf15Reader.read(uploaded_file, errors='ignore')
                text_content = PlaintextWriter.write(temp).read()
            elif get_file_type(name_of_upload_file) == ".txt":
                text_content = uploaded_file.read()
            DOM_of_content = parser.parse(text_content.decode('utf-8'))
            doc = Document(name=DOM_of_content.name, content=DOM_of_content.to_xml(), uploaded_date=uploaded_date,
                           file=uploaded_file)
            doc.save()
            return HttpResponseRedirect(reverse('document:list'))
        else:
            error_message = 'Please select a file.'

    form = UploadForm()
    return render(request, 'document/upload.html', {'form': form, 'error_message': error_message})


def list(request):
    return render(request, 'document/list.html', {'documents': Document.objects.all()})


def law_detail(request, doc_id):
    doc = get_object_or_404(Document, pk=doc_id)
    html_content = XsltTransformer.transform_to_html(doc.content.encode('utf-8'))
    return render(request, 'document/document_view.html',
                  {'document': doc, 'content': html_content, 'document_id': doc_id})


def wrap_text_in_tag(request):
    if request.method == 'POST':
        form = WrapTextForm(request.POST)
        if form.is_valid():
            doc_id = int(request.POST.get('document_id'))
            object_id = request.POST.get('article_item_id')
            start_position = int(request.POST.get('start_position'))
            end_position = int(request.POST.get('length')) + start_position
            reference_url = request.POST.get('reference_url')

            if end_position > start_position > -1:
                document = Document.objects.get(id=doc_id)
                document_content = document.content.encode('utf-8')

                add_reference = AddReference()
                mxml = add_reference.add_node_reference(document_content, object_id, start_position, end_position)

                document.content = mxml
                document.save()

    return render(request, 'document/list.html', {'documents': Document.objects.all()})
