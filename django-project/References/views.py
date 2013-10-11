from document.models import Document
from document.views import render
from References.models import References
from References.forms import WrapTextForm

def wrap_text_in_tag(request):
	if request.method == 'POST':
		form = WrapTextForm(request.POST)
		if form.is_valid():

			#try:
			ref = References()
			ref.reference_document_id = Document(request.POST.get('reference_document_id'))
			ref.reference_element = request.POST.get('reference_element')
			ref.linked_document_id = Document(request.POST.get('linked_document_id'))
			ref.linked_element = request.POST.get('linked_element')

			ref.save()
			#except:
				#raise StandardError('Except')

	return render(request, 'document/list.html', {'documents': Document.objects.all()})
