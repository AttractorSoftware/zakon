from string import replace
from django.core.files.uploadedfile import UploadedFile
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from document.rtfparser import RTFParser
from document.xslt_converter.converter import XsltTransformer
from forms import UploadForm
from models import Document
from law_parser.dom_parser import Parser


def get_file_type(url):
    file_types = [".txt", ".rtf"]
    name_file = str(url)
    for i in file_types:
        if name_file.endswith(i):
            return i


def get_text_content(name_of_upload_file, uploaded_file):
    parser = RTFParser()
    if get_file_type(name_of_upload_file) == ".rtf":
        temp = uploaded_file.read()
        text_content = parser.parse(temp)
    elif get_file_type(name_of_upload_file) == ".txt":
        text_content = uploaded_file.read()
    return text_content


def upload_file(request):
    form = UploadForm(request.POST, request.FILES)
    if form.is_valid():
        name_of_upload_file = UploadedFile(request.FILES['doc_file'])
        uploaded_date = timezone.now()
        uploaded_file = request.FILES['doc_file']
        parser = Parser()
        dom_of_content = parser.parse(get_text_content(name_of_upload_file, uploaded_file))
        doc = Document(name=dom_of_content.name, content=dom_of_content.to_xml(), uploaded_date=uploaded_date,
                       file=uploaded_file)
        doc.save()
        return HttpResponseRedirect(reverse('document:list'))
    else:
        return HttpResponseRedirect(reverse("document:upload_view"))


def list(request):
    return render(request, 'document/list.html', {'documents': Document.objects.all()})


def nl2br(content):
    return replace(content, "\n", "<br />")


def law_detail(request, doc_id):
    doc = get_object_or_404(Document, pk=doc_id)
    html_content = nl2br(XsltTransformer.transform_to_html(doc.content.encode('utf-8')))
    return render(request, 'document/document_view.html',
                  {'document': doc, 'content': html_content, 'document_id': doc_id})


def upload_view(request):
    error_message = ''
    form = UploadForm()
    return render(request, 'document/upload.html', {'form': form, 'error_message': error_message})
