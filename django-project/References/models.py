from django.db import models
from document.models import Document


class Reference(models.Model):
	reference_document = models.ForeignKey(Document, related_name='+')
	reference_element = models.CharField(max_length=20)
	linked_document = models.ForeignKey(Document, related_name='+')
	linked_element = models.CharField(max_length=20)