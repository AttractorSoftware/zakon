from django.core.files.uploadedfile import UploadedFile
from django.http import  HttpResponse
from django.shortcuts import render
from django.utils import timezone
from forms import UploadForm
from models import Document

def upload_file(request):

    error_message = ''
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc_name = UploadedFile(request.FILES['doc_file'])
            # Read content of uploaded file. Must be changed latter
            doc_content = UploadedFile(request.FILES['doc_file']).read()
            #Read an information to fill data base row
            doc_uploaded_date = timezone.now()
            doc = request.FILES['doc_file']
            new_doc = Document(name = doc_name, content = doc_content, uploaded_date = doc_uploaded_date, file = doc)
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

