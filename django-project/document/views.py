from django.core.files.uploadedfile import UploadedFile
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from forms import UploadForm
from models import Document
from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.plaintext.writer import PlaintextWriter
from LawParser.LawHtmlParser import LawHtmlParser
import document.urls

def upload_file(request):

    error_message = ''
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc_name = UploadedFile(request.FILES['doc_file'])
            doc_uploaded_date = timezone.now()
            doc = request.FILES['doc_file']

            result = Rtf15Reader.read(request.FILES['doc_file'])
            parser = LawHtmlParser(PlaintextWriter.write(result).read())
            parsed_doc_content = parser.get_parsed_text()
            new_doc = Document(name = doc_name, content = parsed_doc_content, uploaded_date = doc_uploaded_date, file = doc)
            new_doc.save()

            return HttpResponseRedirect(reverse('document:list'))
        else:
            error_message = 'Please select a file.'

    form = UploadForm()
    return render(request, 'document/upload.html', {'form': form, 'error_message': error_message})

def list(request):

    return render(request, 'document/list.html', {'documents':Document.objects.all()})

def law_detail(request, doc_id):
    law = get_object_or_404(Document, pk=doc_id)
    return render(request, 'document/document_view.html', {'document':law})