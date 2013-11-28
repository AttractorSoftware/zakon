from django.db import models
from document.models import Document


class Reference(models.Model):
    source_document = models.ForeignKey(Document, related_name='+')
    source_element = models.CharField(max_length=20)
    target_document = models.ForeignKey(Document, related_name='+')
    target_element = models.CharField(max_length=20)