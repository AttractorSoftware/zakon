from django.db import models
from document.models import Document


class References(models.Model):
	reference_document_id = models.ForeignKey(Document, related_name='+')
	reference_element = models.CharField(max_length=20)
	linked_document_id = models.ForeignKey(Document, related_name='+')
	linked_element = models.CharField(max_length=20)