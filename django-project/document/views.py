from django.core.files.uploadedfile import UploadedFile
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from forms import UploadForm
from models import Document
from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.xhtml.writer import XHTMLWriter
import os

def upload_file(request):

    error_message = ''
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc_name = UploadedFile(request.FILES['doc_file'])
            # Read content of uploaded file. Must be changed later
            doc_content = UploadedFile(request.FILES['doc_file']).read()
            #Read an information to fill data base row
            doc_uploaded_date = timezone.now()
            doc = request.FILES['doc_file']



            new_doc = Document(name = doc_name, content = '', uploaded_date = doc_uploaded_date, file = doc)
            new_doc.save()

            result = Rtf15Reader.read(open(os.path.realpath('')+new_doc.file.url, "rb"))
            new_doc.content = XHTMLWriter.write(result, pretty=True).read()
            new_doc.save()
            return render(request, 'document/list.html', {'documents':Document.objects.all()})
        else:
            #Fill the error message
            error_message = 'Please select a file.'

    form = UploadForm()
    #render to the "upload" page
    return render(request, 'document/upload.html', {'form': form, 'error_message': error_message})

def list(request):

    return render(request, 'document/list.html', {'documents':Document.objects.all()})

def law_detail(request, doc_id):
    law = get_object_or_404(Document, pk=doc_id)
    return render(request, 'document/document_view.html', {'document':law})