from django.db import models

# Create your models here.
class Document(models.Model):
    name = models.CharField(max_length=300)
    content = models.TextField()
    upload_date = models.DateTimeField()