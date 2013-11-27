import os
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
import time


def get_file_type(url):
    file_types = [".txt", ".rtf"]
    name_file = str(url)
    for i in file_types:
        if name_file.endswith(i):
            return i


def get_text_content(name_of_upload_file, uploaded_file, fileType=False):
    parser = RTFParser()
    text_content = False
    if fileType == 'rtf':
        temp = open(uploaded_file, 'r').read()
        text_content = parser.parse(temp)
    else:
        if get_file_type(name_of_upload_file) == ".rtf":
            temp = uploaded_file.read()
            text_content = parser.parse(temp)
        elif get_file_type(name_of_upload_file) == ".txt":
            text_content = uploaded_file.read()
    return text_content


def handle_uploaded_temp_file(f, fileFullPath):
    with open(fileFullPath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload_file(request):
    temp_dir = 'temp_uploads'
    uploaded_date = timezone.now()
    parser = Parser()
    form = UploadForm(request.POST, request.FILES)
    if form.is_valid():
        name_of_upload_file = UploadedFile(request.FILES['doc_file'])
        uploaded_file = request.FILES['doc_file']
        dom_of_content = parser.parse(get_text_content(name_of_upload_file, uploaded_file))
        if parser.has_errors():
            if not os.path.isdir(temp_dir):
                os.makedirs(temp_dir, 0777);
            tmp_file_name = str(int(time.time())) + name_of_upload_file._name
            handle_uploaded_temp_file(uploaded_file, temp_dir + '/' + tmp_file_name)
            return render(
                request,
                'document/confirmUploadAnyway.html',
                {
                    'error_messages': parser.get_errors(),
                    'upload_anyway_file_name': tmp_file_name
                }
            )
        else:
            doc = Document(
                name=dom_of_content.name,
                content=dom_of_content.to_xml(),
                uploaded_date=uploaded_date,
                file=uploaded_file
            )
            doc.save()
        return HttpResponseRedirect(reverse('document:list'))
    elif request.POST.get('upload_anyway_file_name', False):
        name_of_upload_file = request.POST['upload_anyway_file_name']
        uploaded_file_path = temp_dir + '/' + name_of_upload_file
        dom_of_content = parser.parse(get_text_content(name_of_upload_file, uploaded_file_path, 'rtf'))
        doc = Document(
            name=dom_of_content.name,
            content=dom_of_content.to_xml(),
            uploaded_date=uploaded_date,
            file=uploaded_file_path
        )
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
    return render(
        request,
        'document/document_view.html',
        {
            'document': doc,
            'content': html_content,
            'document_id': doc_id
        }
    )


def upload_view(request):
    error_message = ''
    form = UploadForm()
    return render(request, 'document/upload.html', {'form': form, 'error_message': error_message})
