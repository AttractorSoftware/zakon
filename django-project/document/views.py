from django.core.files.uploadedfile import UploadedFile
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.plaintext.writer import PlaintextWriter

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


def is_valid_xml_char_ordinal(i):
        return (
            0x20 <= i <= 0xD7FF
            or i in (0x9, 0xA, 0xD)
            or 0xE000 <= i <= 0xFFFD
            or 0x10000 <= i <= 0x10FFFF
            )


def clean_xml_string(s):
    return ''.join(c for c in s if is_valid_xml_char_ordinal(ord(c)))


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
            DOM_of_content = parser.parse(clean_xml_string(text_content.decode('utf-8')))
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


