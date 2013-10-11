from django.db import models


class Document(models.Model):
	name = models.CharField(max_length=300)
	content = models.TextField()
	uploaded_date = models.DateTimeField()
	#Files will be saved at media/documents/"uploaded year"/"uploaded month"/"uploaded day"/file
	file = models.FileField(upload_to="documents/")


class References(models.Model):
	reference_document_id = models.ForeignKey(Document, related_name='+')
	reference_element = models.CharField(max_length=20)
	linked_document_id = models.ForeignKey(Document, related_name='+')
	linked_element = models.CharField(max_length=20)
