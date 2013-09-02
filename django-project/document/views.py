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
                  {'document': doc, 'content': html_content, 'document_id': doc_id});


def wrap_text_in_tag(request):
    if request.method == 'POST':
        form = WrapTextForm(request.POST)
        if form.is_valid():
            doc_id = int(request.POST.get('document_id'))
            object_id = request.POST.get('article_item_id')
            start_position = int(request.POST.get('start_position'))
            end_position = int(request.POST.get('end_position'))
            reference_url = request.POST.get('reference_url')
            doc = Document.objects.get(id=doc_id)

            doc_content = doc.content.encode('utf-8')
            xml_parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')

            myxml = etree.fromstring(doc_content, parser=xml_parser)

            expr = ".//*[@id='" + object_id + "']"

            for item in myxml.xpath(expr):
                if item.attrib['id'] == str(object_id):
                    text = item.text
                    item.text = ""
                    print text, start_position
                    item.text = text[:start_position]
                    element = etree.Element('reference', document_id=str(doc_id), object_id=object_id)
                    element.text = text[start_position:end_position]
                    item.insert(0, element)
                    element.tail = text[end_position:]
                    # print 'finish_text => ', stringify_children(item)

            doc.content = etree.tostring(myxml, encoding='utf-8')

            # print doc.content

            doc.save()

    return render(request, 'document/list.html', {'documents': Document.objects.all()})



def _add_node_reference(node, start_position, end_position):
    # return "".join([x for x in node.itertext()])
    parts = ([node.text] +
             list(chain(*([tostring(c)] for c in node.getchildren()))) +
             [node.tail])

    text = node.text



def _add_node(node, text):
    pass